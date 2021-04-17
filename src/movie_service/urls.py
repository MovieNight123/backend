from django.urls import path, include
from rest_framework import routers

from .views import AuthorizationViewSet, MovieViewSet

router = routers.SimpleRouter()
router.register(r'auth', AuthorizationViewSet, basename='auth')
router.register(r'movie_api', MovieViewSet, basename='movie')

urlpatterns = [
    path('auth/', include(router.urls)),
]
