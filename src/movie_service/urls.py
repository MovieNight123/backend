from django.urls import path, include
from rest_framework import routers

from .views import AuthorizationViewSet

router = routers.SimpleRouter()
router.register(r'auth', AuthorizationViewSet, basename='auth')

urlpatterns = [
    path('auth/', include(router.urls)),
]
