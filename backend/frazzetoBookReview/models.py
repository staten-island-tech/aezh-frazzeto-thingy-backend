from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    is_instructor = models.BooleanField(default=False)

class Authors(models.Model):
    name = models.CharField(max_length=50)

class Books(models.Model):
    author = models.ForeignKey(Authors,on_delete=models.CASCADE,related_name="books")
    img = models.URLField()
    genre = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    pageLength = models.IntegerField()
    reviewCount = models.IntegerField()

class Reviews(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE, related_name="reviews")
    stars =models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    textReview =models.CharField(max_length=500)
    book = models.ForeignKey(Books,on_delete=models.CASCADE, related_name="reviews")

class Courses(models.Model):
    name = models.CharField(max_length=100)
    classcode = models.CharField(max_length=9, unique=True)
    students = models.ManyToManyField("auth.User", related_name="enrolled_courses")
    instructor = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="courses")
    archived = models.BooleanField(default=False)
    period = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(9)])

class AssignmentReviews(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="assignment_reviews")
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    textReview = models.CharField(max_length=500)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="assignment_reviews")