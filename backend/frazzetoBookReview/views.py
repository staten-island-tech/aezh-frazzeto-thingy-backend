from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from frazzetoBookReview.serializers import *
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from frazzetoBookReview.models import Books
from django.db.models import Avg, Count
from rest_framework.permissions import AllowAny

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class BookPagination(PageNumberPagination):
    page_size = 20
class BookView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        return Books.objects.annotate(
            averageRating=Avg("reviews__stars"),
            reviewCount=Count("reviews")
        )
    def addbook(request):
        if request.method == 'POST':
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CourseView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    def getandpost(request):
        if request.method == 'GET':
            courses = Courses.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(instructor=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentReviewView(generics.ListCreateAPIView):
    queryset = AssignmentReviews.objects.all()
    serializer_class = AssignmentReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class userView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer