from django.urls import path, include
from rest_framework import routers

from .views import AuthorizationViewSet, MovieListViewSet, MovieApiView

router = routers.SimpleRouter()
router.register(r'auth', AuthorizationViewSet, basename='auth')
router.register(r'movie-list', MovieListViewSet, basename='movie_list')

urlpatterns = [
    path('movie/<int:pk>/', MovieApiView.as_view()),
] + router.urls
