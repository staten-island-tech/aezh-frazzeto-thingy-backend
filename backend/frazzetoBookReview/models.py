from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.


class Authors(models.Model):
    name = models.CharField(max_length=50)

class Books(models.Model):
    author = models.ForeignKey(Authors,on_delete=models.CASCADE,related_name="books")
    genre = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    pageLength = models.IntegerField()
    reviewCount = models.IntegerField

class Reviews(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE, related_name="reviews")
    stars =models.IntegerField(validators=[ MinValueValidator(1),MaxValueValidator(5)])
    textReview =models.CharField(max_length=400)
    book = models.ForeignKey(Books,on_delete=models.CASCADE, related_name="reviews")




    
