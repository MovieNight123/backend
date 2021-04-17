from django.contrib.auth.models import User as BaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(BaseUser):
	name = models.CharField(max_length=128)
	photo = models.ImageField(null=True)


class Genre(models.Model):
	name = models.CharField(max_length=15)

	class Meta:
		verbose_name = "Genre"
		verbose_name_plural = "Genres"

	def __str__(self):
		return self.name


class Movie(models.Model):
	imdb_id = models.CharField(max_length=16, unique=True)
	movie_id = models.PositiveIntegerField(unique=True, db_index=True)
	title = models.CharField(max_length=128)
	picture = models.ImageField(null=True)
	poster_path = models.CharField(max_length=256)
	overview = models.CharField(max_length=1024)
	vote_average = models.FloatField()
	vote_count = models.IntegerField()
	popularity = models.FloatField()
	language = models.CharField(max_length=2)
	runtime = models.SmallIntegerField()
	year = models.SmallIntegerField()
	director_id = models.CharField(max_length=16, null=True)
	director_name = models.CharField(max_length=128, null=True)
	budget = models.IntegerField()
	revenue = models.IntegerField()
	collection_id = models.IntegerField(null=True)

	class Meta:
		verbose_name = "Movie"
		verbose_name_plural = "Movies"

	def __str__(self):
		return self.title


class MovieGenre(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_genres")
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="movie_genres")


class Rating(models.Model):
	value = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")


class WatchListItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlist_items")


class Review(models.Model):
	TYPES = (
		('POSITIVE', 'POSITIVE'),
		('NEGATIVE', 'NEGATIVE'),
	)

	LANGUAGES = (
		('EN', 'EN'),
		('RU', 'RU'),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
	text = models.CharField(max_length=1024)
	type = models.CharField(choices=TYPES, max_length=20)
	language = models.CharField(choices=LANGUAGES, max_length=2)
	created_at = models.DateTimeField(auto_now=True)
