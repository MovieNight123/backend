import pandas as pd

from movie_service.models import Rating, User


def get_dataset():
	ratings = Rating.objects.all()
	user_ids = [rating.user.id for rating in ratings]
	movie_ids = [rating.movie.movie_id for rating in ratings]
	values = [rating.value for rating in ratings]
	dataset = pd.DataFrame(data={"user": user_ids, "movie": movie_ids, "rating": values})
	return dataset


def get_similarity_matrix(dataset):
	matrix = dataset.pivot_table(index="user", columns="movie", values="rating")
	return matrix


def get_recommendations(matrix, user, indices):
	try:
		idx = indices[user.id]
		user_movies = matrix[idx]
		similar_movies = matrix.corrwith(user_movies)
		correlation_coefficients = pd.DataFrame(similar_movies, columns=["correlation"])
		correlation_coefficients.dropna(inplace=True)
		correlation_coefficients.sort_values("correlation", ascending=False)
		correlation_coefficients = correlation_coefficients.head(100)
		return list(correlation_coefficients["movie"])
	except:
		return []


def run():
	print("Processing dataset...")
	dataset = get_dataset()
	print("Creating similarity matrix...")
	matrix = get_similarity_matrix(dataset)
	indices = pd.Series(matrix.index, index=matrix["user"])
	print("Updating recommendations...")
	users = User.objects.all()
	for user in users:
		get_recommendations(matrix, user, indices)
	print("Done.")
