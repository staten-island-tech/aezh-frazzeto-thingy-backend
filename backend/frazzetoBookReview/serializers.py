from rest_framework import serializers
from frazzetoBookReview.models import Authors, Reviews, Books, User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["id", "name"]

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "user", "stars", "textReview", "book"]

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ["id", "author", "averageRating", "genre", "title", "pageLength"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "reviews"]