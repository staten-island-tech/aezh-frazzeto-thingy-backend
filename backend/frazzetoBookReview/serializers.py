from rest_framework import serializers
from frazzetoBookReview.models import Authors, Reviews, Books, User
from django.db.models import Avg
from django.contrib.auth import authenticate

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["id", "name"]


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "user", "stars", "textReview", "book"]
        read_only_fields = ["user"]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    averageRating = serializers.FloatField(read_only=True)
    reviewCount = serializers.IntegerField(read_only=True)
    class Meta:
        model = Books
        fields = ["id", "author", "averageRating", "genre", "title", "pageLength", "reviewCount"]



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('email', '').split('@', 1)[0],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user