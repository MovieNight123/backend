from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(BaseUser):
    name = models.CharField(max_length=128)
    photo = models.ImageField(null=True)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    picture = models.ImageField(null=True)
    description = models.CharField(max_length=1024)
    average_rating = models.FloatField()


class Rating(models.Model):
    value = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class WatchListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Review(models.Model):
    TYPES = (
        ('POSITIVE', 'POSITIVE'),
        ('NEGATIVE', 'NEGATIVE'),
    )

    LANGUAGES = (
        ('EN', 'EN'),
        ('RU', 'RU'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    type = models.CharField(choices=TYPES, max_length=20)
    language = models.CharField(choices=LANGUAGES, max_length=2)
    created_at = models.DateTimeField(auto_now=True)
