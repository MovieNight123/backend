from ast import literal_eval

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from movie_service.models import Movie

from .parse_movies import get_movies


def weighted_rating(row, min_votes, vote_mean):
	v = row["vote_count"]
	r = row["vote_average"]
	return (v / (v + min_votes) * r) + (min_votes / (min_votes + v) * vote_mean)


def count_popularity(movies):
	vote_mean = movies["vote_average"].mean()
	min_votes = movies["vote_count"].quantile(0.65)
	for index, row in movies.iterrows():
		try:
			movie_object = Movie.objects.get(movie_id=int(row["id"]))
			movie_object.popularity = weighted_rating(row, min_votes, vote_mean)
			movie_object.save()
		except ObjectDoesNotExist:
			pass


def get_key_words(movies):
	keywords = pd.read_csv("scripts/data/keywords.csv")
	movies = movies.astype({"id": int})
	movies = movies.merge(keywords, on="id")
	movies["keywords"] = movies["keywords"].apply(literal_eval)
	cnt = 0
	for index, row in movies.iterrows():
		words = row["keywords"][:6]
		words = [word["name"].lower().replace(" ", "") for word in words]
		words = " ".join(words)
		try:
			movie_object = Movie.objects.get(movie_id=int(row["id"]))
			movie_object.keywords = words
			movie_object.save()
		except ObjectDoesNotExist:
			cnt += 1
			pass
	print(f"Passed {cnt} times")


def run():
	print("Reading movies dataset...")
	movies = get_movies()
	print("Updating popularity...")
	count_popularity(movies)
	print("Updating keywords...")
	get_key_words(movies)
