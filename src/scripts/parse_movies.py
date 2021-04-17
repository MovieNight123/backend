import json

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from movie_service.models import Movie, Genre, MovieGenre


def get_movies():
	movies = pd.read_csv("scripts/data/movies_metadata.csv", low_memory=False)
	movies = movies[movies["vote_count"] >= 40]
	movies = movies[movies["status"] == "Released"]
	movies = movies[movies["overview"].notna()]
	movies = movies[movies["release_date"].notna()]
	movies = movies[movies["video"] == False]

	movies.drop("adult", inplace=True, axis=1)
	movies.drop("homepage", inplace=True, axis=1)
	movies.drop("original_title", inplace=True, axis=1)
	movies.drop("production_companies", inplace=True, axis=1)
	movies.drop("production_countries", inplace=True, axis=1)
	movies.drop("status", inplace=True, axis=1)
	movies.drop("tagline", inplace=True, axis=1)
	movies.drop("video", inplace=True, axis=1)

	movies.iat[7400, 4] = "tt1325753"
	movies = movies.drop_duplicates()
	assert len(movies) == 10368, "Invalid total number"
	return movies


def validate_movies(movies):
	assert len(movies) == 10368, "Invalid total number"
	cnt = [0] * 16
	for i in range(len(movies)):
		for j in range(16):
			if str(movies.iloc[i, j]) == "nan":
				cnt[j] += 1

	for i in range(1, 16):
		assert cnt[i] == 0, "NaN in column {}".format(i)


def get_collection_id(row):
	try:
		col = row["belongs_to_collection"]
		col = json.loads(col.replace("'", '"'))
		return int(col["id"])
	except:
		return None


def get_directors(movies):
	imdb_ids = set()
	for index, row in movies.iterrows():
		imdb_ids.add(row["imdb_id"])
	print("Parsed imbd_ids")

	dirs = pd.read_csv("scripts/data/title.crew.tsv", sep="\t", header=0)
	movie_data = {}
	directors_data = {}
	for index, row in dirs.iterrows():
		tconst = row["tconst"]
		if tconst in imdb_ids and tconst not in movie_data:
			nconst = row["directors"].split(",")[0]
			nconst = nconst if nconst[:2] == "nm" else None
			movie_data[tconst] = {"nconst": nconst}

			if nconst is not None:
				if nconst not in directors_data:
					directors_data[nconst] = [tconst]
				else:
					directors_data[nconst].append(tconst)
	print("Parsed tconsts")

	names = pd.read_csv("scripts/data/name.basics.tsv", sep="\t", header=0)
	for index, row in names.iterrows():
		nconst = row["nconst"]
		if nconst in directors_data:
			for tconst in directors_data[nconst]:
				movie_data[tconst]["name"] = row["primaryName"]
	print("Parsing directors done")

	return movie_data


def get_genres(row, movie_object):
	genres = row["genres"].replace("'", '"')
	genres = json.loads(genres)
	assert type(genres) == list, "Invalid type of genres. Must be list"

	result = []
	for genre in genres:
		genre_name = genre["name"]
		genre_object, created = Genre.objects.get_or_create(name=genre_name)
		result.append(MovieGenre(movie=movie_object, genre=genre_object))
	return result


def fill_movies_db(movies, dirs):
	imdb_ids = set()
	movies_db = []

	for index, row in movies.iterrows():
		imdb_id = row["imdb_id"]
		if imdb_id in imdb_ids or imdb_id not in dirs:
			continue
		if index % 500 == 0:
			print(f"Processed {index} rows...")
		imdb_ids.add(imdb_id)
		movie_id = int(row["id"])
		title = row["title"]
		poster_path = row["poster_path"]
		overview = row["overview"]
		vote_average = float(row["vote_average"])
		vote_count = int(row["vote_count"])
		popularity = float(row["popularity"])
		language = row["original_language"]
		runtime = int(row["runtime"])
		year = int(row["release_date"][:4])
		director_id = dirs[imdb_id]["nconst"]
		director_name = dirs[imdb_id]["name"] if "name" in dirs[imdb_id] else None
		budget = int(row["budget"])
		revenue = int(row["revenue"])
		collection_id = get_collection_id(row)

		movies_db.append(Movie(imdb_id=imdb_id, movie_id=movie_id, title=title,
							   poster_path=poster_path, overview=overview,
							   vote_average=vote_average, vote_count=vote_count,
							   popularity=popularity, language=language,
							   runtime=runtime, year=year, director_id=director_id,
							   director_name=director_name, budget=budget,
							   revenue=revenue, collection_id=collection_id)
						 )

	Movie.objects.bulk_create(movies_db)


def fill_genres_db(movies):
	imdb_ids = set()
	genres_db = []

	for index, row in movies.iterrows():
		imdb_id = row["imdb_id"]
		if imdb_id in imdb_ids:
			continue
		if index % 500 == 0:
			print(f"Processed {index} rows...")
		imdb_ids.add(imdb_id)
		try:
			movie_object = Movie.objects.get(imdb_id=imdb_id)
			movie_genres = get_genres(row, movie_object)
			genres_db.extend(movie_genres)
		except ObjectDoesNotExist:
			pass
	MovieGenre.objects.bulk_create(genres_db)


def run():
	print("Processing dataset...")
	movies = get_movies()
	print("Validating dataset...")
	validate_movies(movies)
	print("Validation OK. Parsing directors...")
	dirs = get_directors(movies)
	print("Filling movies db...")
	fill_movies_db(movies, dirs)
	print("Filling genres db...")
	fill_genres_db(movies)
	print("Done.")
