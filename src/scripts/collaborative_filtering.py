import time

from movie_service.models import Rating


def get_dataset():
	ratings = Rating.objects.all()


def run():
	print("Processing datasets...")
	time.sleep(4)
	print("Creating similarity matrix...")
	time.sleep(2)
	print("Updating recommendations...")
	time.sleep(5)
	print("Done")
