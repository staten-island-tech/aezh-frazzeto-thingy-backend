from rest_framework import serializers
from frazzetoBookReview.models import Authors, Courses, Reviews, Books, User
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
    img = serializers.URLField(required=True)
    class Meta:
        model = Books
        fields = ["id", "author", "img", "averageRating", "genre", "title", "pageLength", "reviewCount"]



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "reviews"]
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, data):
        return User.objects.create_user(**data)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
            user = authenticate(
                username=data["username"],
                password=data["password"]
            )

            if user is None:
                raise serializers.ValidationError(
                    "Invalid username or password"
                )

            data["user"] = user
            return data

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)
    students = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Courses
        fields = ["id", "name", "students", "instructor"]