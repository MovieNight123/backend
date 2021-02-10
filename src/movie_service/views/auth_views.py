from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import mixins, viewsets, serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView


class AuthorizationViewSet(viewsets.ViewSet):
    def post(self, request):
        try:
            user = User.objects.create_user(username=request.data.get('username'),
                                            email=request.data.get('email'),
                                            password=request.data.get('password'))
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})

    @action(detail=False, methods='DELETE')
    def logout(request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)