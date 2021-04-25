from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from ..models import Movie, Genre, MovieGenre, Rating, User
from ..serializers import MovieSerializer, RatingSerializer


class MovieListViewSet(viewsets.ModelViewSet):
	http_method_names = ["get"]
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

	@action(methods=["GET"], detail=True)
	def recommendations(self, request, pk=None):
		print("here")
		movie_object = self.get_object()
		recommendations = movie_object.content_based_recommendations
		recommendations = [int(rec) for rec in recommendations.split()]
		recommendations = Movie.objects.filter(movie_id__in=recommendations)
		serializer = self.get_serializer(recommendations, many=True)
		return Response(serializer.data)


class MovieApiView(generics.RetrieveAPIView):
	permission_classes = (AllowAny,)
	serializer_class = MovieSerializer
	queryset = Movie.objects.all()

	def get(self, request, *args, **kwargs):
		movie = Movie.objects.get(movie_id=kwargs['pk'])
		return Response(MovieSerializer(movie).data)


class RatingApiView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def post(self, request, *args, **kwargs):
        movie = Movie.objects.get(movie_id=request.data.get('movie_id'))
        rating_value = request.data.get('rating_value')

        try:
            user = User.objects.get(id=request.user.id)
        except:
            user = User.objects.create(id=request.user.id, name='n')
        print(user, request.user.id)

        if movie and user and rating_value:
            Rating.objects.create(user=user, movie=movie, value=rating_value)

            votes_sum = movie.vote_average * movie.vote_count + rating_value
            movie.vote_count += 1
            movie.vote_average = votes_sum / movie.vote_count
            movie.save()

            return Response('ok')
        return Response('err')
