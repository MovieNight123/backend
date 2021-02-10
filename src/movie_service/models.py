from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)

class Rate(models.Model):
    rate = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

