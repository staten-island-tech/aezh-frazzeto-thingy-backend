from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from frazzetoBookReview.models import AssignmentReviews, Authors, Courses, Reviews, Books, UserProfile
from django.db.models import Avg
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
import random
import string

class UserSerializer(serializers.ModelSerializer):
    is_instructor = serializers.BooleanField(source="user_profile.is_instructor", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_instructor"]

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Authors
        fields = ["id", "name"]

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "user", "stars", "textReview", "book", "isAssignment", "assignment"]
        read_only_fields = ["user", "isAssignment"]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    averageRating = serializers.FloatField(read_only=True)
    reviewCount = serializers.IntegerField(read_only=True)
    img = serializers.URLField(required=True)
    class Meta:
        model = Books
        fields = ["id", "author", "img", "averageRating", "genre", "title", "pageLength", "reviewCount", "featured"]
    def create(self, validated_data):
        author_data = validated_data.pop("author")

        author, created = Authors.objects.get_or_create(
            name=author_data["name"]
        )

        book = Books.objects.create(
            author=author,
            **validated_data
        )

        return book
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=validated_data["password"],
            )
        except IntegrityError:
            raise serializers.ValidationError({"email": "An account with this email already exists."})
        UserProfile.objects.get_or_create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)
    students = serializers.StringRelatedField(many=True, read_only=True)
    classcode = serializers.CharField(read_only=True)

    class Meta:
        model = Courses
        fields = ["id", "name", "classcode", "students", "instructor", "period", "isArchived"]

    def create(self, validated_data):
        validated_data["classcode"] = self._generate_unique_classcode()
        return super().create(validated_data)

    def _generate_unique_classcode(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            if not Courses.objects.filter(classcode=code).exists():
                return code

class AssignmentReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentReviews
        fields = ["id", "course", "book", "student", "assigned_by", "due_date", "created_at"]
        read_only_fields = ["assigned_by", "created_at"]

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        return data
