from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Movie, Genre, MovieGenre
from ..serializers import MovieSerializer


class MovieListViewSet(mixins.ListModelMixin,
					   mixins.CreateModelMixin,
					   mixins.RetrieveModelMixin,
					   mixins.UpdateModelMixin,
					   mixins.DestroyModelMixin,
					   viewsets.GenericViewSet):
	permission_classes = (AllowAny,)
	serializer_class = MovieSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		return Movie.objects.all()

	def list(self, request, *args, **kwargs):
		filter_start_year = request.GET.get('start_year', 1999)
		filter_end_year = request.GET.get('end_year', 1999)
		filter_title = request.GET.get('title', '')
		sort_by = request.GET.get('sort_by', 'year')
		filter_genre = request.GET.get('genre')

		movies = Movie.objects.filter(year__gte=filter_start_year, year__lte=filter_end_year,
									  title__contains=filter_title).order_by(f'-{sort_by}')

		if filter_genre:
			genre = Genre.objects.get(name=filter_genre)

			if genre:
				movie_ids = []

				for movie in movies:
					movie_genre = MovieGenre.objects.filter(movie=movie, genre=genre)
					if movie_genre:
						movie_ids.append(movie.movie_id)

			movies = Movie.objects.filter(movie_id__in=movie_ids)

		return Response(MovieSerializer(movies, many=True).data)


class MovieApiView(generics.RetrieveAPIView):
	permission_classes = (AllowAny,)
	serializer_class = MovieSerializer
	queryset = Movie.objects.all()

	def get(self, request, *args, **kwargs):
		movie = Movie.objects.get(movie_id=kwargs['pk'])
		return Response(MovieSerializer(movie).data)
