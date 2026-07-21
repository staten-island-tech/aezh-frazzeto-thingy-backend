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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
            }
        )
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
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
class ReviewView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
