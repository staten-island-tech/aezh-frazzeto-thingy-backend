from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from frazzetoBookReview.serializers import *
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from frazzetoBookReview.models import Books
from django.db.models import Avg, Count, Q
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


# Permission Checks
class IsCourseInstructor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == "GET":
            return True
        if request.method == "POST":
            course_id = request.data.get("course")
            if not course_id:
                return False
            return Courses.objects.filter(id=course_id, instructor=request.user).exists()
        return False

class CanCreateCourseAndAddBookAndFeatureBook(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == "GET":
          return True
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
          return (request.user.is_authenticated and hasattr(request.user, "user_profile") and request.user.user_profile.is_instructor)

class CanDeleteReview(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        if (hasattr(request.user, "user_profile") and request.user.user_profile.is_instructor):
            return True
        return False
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class BookPagination(PageNumberPagination):
    page_size = 10
class BookView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [CanCreateCourseAndAddBookAndFeatureBook]

    def get_queryset(self):
        queryset = Books.objects.annotate(
            averageRating=Avg("reviews__stars"),
            reviewCount=Count("reviews")
        ).order_by("id")
        title = self.request.query_params.get("title")
        genre = self.request.query_params.get("genre")
        author = self.request.query_params.get("author")
        book_id = self.request.query_params.get("id")
        featured = self.request.query_params.get("featured")
        if book_id:
            queryset = queryset.filter(id=book_id)
            return queryset
        if featured is not None:
            if featured.lower() == "true":
                queryset = queryset.filter(featured=True)
            elif featured.lower() == "false":
                queryset = queryset.filter(featured=False)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if author:
            queryset = queryset.filter(author__name__icontains=author)
        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [CanCreateCourseAndAddBookAndFeatureBook]

class ReviewPagination(PageNumberPagination):
    page_size = 3

class ReviewView(generics.ListCreateAPIView):
    serializer_class = ReviewsSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        queryset = Reviews.objects.all()
        book_id = self.request.query_params.get("book")
        if book_id:
            queryset = queryset.filter(book=book_id)
        return queryset

    def perform_create(self, serializer):
        assignment = serializer.validated_data.get("assignment")
        serializer.save(user=self.request.user, isAssignment=assignment is not None)

class AssignmentReviewView(generics.ListCreateAPIView):
    serializer_class = AssignmentReviewsSerializer
    permission_classes = [IsCourseInstructor]

    def get_queryset(self):
        user = self.request.user
        return AssignmentReviews.objects.filter(Q(assigned_by=user) | Q(student=user))

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class CourseView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CanCreateCourseAndAddBookAndFeatureBook]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class JoinCourseView(APIView):
    def post(self, request):
        classcode = request.data.get("classcode")
        if not classcode:
            return Response({"error": "classcode is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Courses.objects.get(classcode=classcode)
        except Courses.DoesNotExist:
            return Response({"error": "No course found with that classcode"}, status=status.HTTP_404_NOT_FOUND)
        if request.user in course.students.all():
            return Response({"error": "Already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(request.user)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [CanDeleteReview]

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        old_refresh = request.data.get("refresh")
        if old_refresh:
            try:
                RefreshToken(old_refresh).blacklist()
            except TokenError:
                pass

        user.set_password(data["new_password"])
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "detail": "Password changed successfully.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
