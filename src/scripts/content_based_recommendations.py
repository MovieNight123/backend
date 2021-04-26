import pandas as pd
from movie_service.models import Movie, MovieGenre
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_genres(movies):
	genres = []
	for movie in movies:
		movie_genres = MovieGenre.objects.filter(movie=movie)
		gs = [mg.genre.name for mg in movie_genres][:2]
		gs = [g.lower().replace(" ", "") for g in gs]
		genres.append(" ".join(gs))
	return genres


def create_soups(titles, keywords, dirs, genres):
	assert len(titles) == len(keywords) == len(dirs) == len(genres)
	soups = []
	for i in range(len(titles)):
		soup = " ".join([titles[i], keywords[i], dirs[i], dirs[i], genres[i]])
		soups.append(soup)
	return soups


def get_dataset():
	movies = Movie.objects.all()
	ids = [movie.movie_id for movie in movies]
	titles = [movie.title.lower().replace(" ", "") for movie in movies]
	keywords = [movie.keywords for movie in movies]
	dirs = [m.director_name.lower().replace(" ", "") if m.director_name is not None else "" for m in movies]
	col_ids = [movie.collection_id for movie in movies]
	genres = get_genres(movies)
	soups = create_soups(titles, keywords, dirs, genres)
	dataset = pd.DataFrame(data={"id": ids, "soup": soups, "collection_id": col_ids})
	return dataset


def get_similarity_matrix(data):
	count = CountVectorizer(stop_words="english")
	count_matrix = count.fit_transform(data["soup"])
	print("Shape:", count_matrix.shape)
	cosine_sim = cosine_similarity(count_matrix, count_matrix)
	return cosine_sim


def get_recommendations(movie_id, indices, cosine_sim):
	try:
		idx = indices[movie_id]
		sim_scores = list(enumerate(cosine_sim[idx]))
		sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
		sim_scores = sim_scores[1:101]
		return [i[0] for i in sim_scores]
	except:
		return []


def update_recommendations(dataset, cosine_sim):
	indices = pd.Series(dataset.index, index=dataset["id"]).drop_duplicates()
	for index, row in dataset:
		recs = get_recommendations(row["id"], indices, cosine_sim)
		recs = Movie.objects.filter(year__gt=1980).filter(movie_id__in=recs)
		recs = list(recs)
		if str(row["collection_id"]) != "nan":
			col_recs = Movie.objects.filter(collection_id=row["collection_id"])
			col_recs = list(col_recs)
			cols = []
			for c in col_recs:
				if c.movie_id != row["imdb_id"]:
					cols.append(c)
			recs.extend(cols)
		recs = list(set(recs))
		recs.sort(key=lambda x: x.popularity, reverse=True)
		if len(recs) < 6:
			print(len(recs), row["id"])
		recs = recs[:6]
		recs = [str(rec.movie_id) for rec in recs]
		recs = " ".join(recs)
		movie_object = Movie.objects.get(movie_id=row["id"])
		movie_object.content_based_recommendations = recs
		movie_object.save()


def run():
	print("Processing dataset...")
	dataset = get_dataset()
	print("Creating similarity matrix...")
	cosine_sim = get_similarity_matrix(dataset)
	print("Updating recommendations...")
	update_recommendations(dataset, cosine_sim)
	print("Done.")
