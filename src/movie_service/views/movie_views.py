import logging
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ..models import Movie
from ..serializers import MovieSerializer


class MovieViewSet(mixins.ListModelMixin,
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
        filter_year = request.GET.get('year', 1999)
        filter_title = request.GET.get('title', '')
        sort_by = request.GET.get('sort_by', 'year')  # todo add sort by popularity
        # todo filter by genre
        movies = Movie.objects.filter(year=filter_year, title__contains=filter_title).order_by(f'-{sort_by}')
        return Response(MovieSerializer(movies, many=True).data)

