import uuid

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from movie_service.models import Movie, User, Rating


def create_users():
	for i in range(270896):
		username = str(uuid.uuid4())[:13]
		email = username + "@kbtu.kz"
		User.objects.create(username=username, email=email, id=i + 1)
	print(f"Created users")


def parse(ratings):
	rating_objects = []
	users = set()
	for index, row in ratings.iterrows():
		user_id = int(row["user_id"])
		users.add(user_id)
		if len(users) == 20001:
			break
		value = int(row["rating"] * 2)
		movie_id = int(row["movie_id"])
		try:
			movie_object = Movie.objects.get(movie_id=movie_id)
			user_object = User.objects.get(id=user_id)
			rating_objects.append(Rating(user=user_object, movie=movie_object, value=value))
		except ObjectDoesNotExist:
			pass
		if index % 100000 == 0:
			print(f"Processed {index} rows. Added {len(rating_objects)} ratings")
	Rating.objects.bulk_create(rating_objects)
	print(f"Created {len(rating_objects)} ratings")


def run():
	print("Creating users...")
	create_users()
	print("Reading ratings dataset...")
	ratings = pd.read_csv("scripts/data/ratings.csv")
	print("Parsing ratings...")
	parse(ratings)
	print("Done.")
