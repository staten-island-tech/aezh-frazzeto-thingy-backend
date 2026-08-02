from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.

class UserProfile(models.Model):
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

class Courses(models.Model):
    name = models.CharField(max_length=100)
    classcode = models.CharField(max_length=9, unique=True)
    students = models.ManyToManyField("auth.User", related_name="enrolled_courses")
    instructor = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="courses")
    period = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(9)])

class AssignmentReviews(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="assignments_reviews")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="assignments")
    student = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="assignments_reviews")
    assigned_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="assignments_created")
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "student", "course")
class Reviews(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="reviews")
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    textReview = models.CharField(max_length=500)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="reviews")
    isAssignment = models.BooleanField(default=False)
    assignment = models.ForeignKey(AssignmentReviews, on_delete=models.SET_NULL, null=True, blank=True, related_name="submitted_review")


