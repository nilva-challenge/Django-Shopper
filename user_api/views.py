from django.utils.decorators import method_decorator

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from user_api.serializers import EmailUserSerializer, EmailAuthTokenSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="create user", request_body=EmailUserSerializer,
    responses={status.HTTP_201_CREATED:
                   openapi.Response('token.key, Type string', )}
))
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = EmailUserSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="get current loged in user",
    responses={status.HTTP_200_OK:
                   openapi.Response('User is', EmailUserSerializer)}
))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Deactivate User", responses={status.HTTP_403_FORBIDDEN:
                                                            openapi.Response('User Deleted')}
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Deactivate User", responses={status.HTTP_403_FORBIDDEN:
                                                            openapi.Response('User Deleted')}
))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deactivate User", responses={status.HTTP_403_FORBIDDEN:
                                                            openapi.Response('User Deleted')}
))
class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update, deactivate an existing user in the system"""
    serializer_class = EmailUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return serializers.ListaGruppi
    #     if self.action == 'retrieve':
    #         return serializers.DettaglioGruppi

    def get_object(self):
        """:return request.user"""
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        return user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN, data='user deactivated')

    def perform_destroy(self, user):
        user.is_active = False
        user.save()

@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deactivate User", responses={status.HTTP_403_FORBIDDEN:
                                                            openapi.Response('User Deleted')}
))
class DeactivateUserView(generics.DestroyAPIView):
    """deactivate an existing user in the system"""
    # serializer_class = CreateUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """:return request.user"""
        user = None
        if self.request and hasattr(self.request, "user"):
            user = self.request.user
        return user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN, data='user deactivated')

    def perform_destroy(self, user):
        user.is_active = False
        user.save()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="get token for a user", request_body=EmailAuthTokenSerializer,
    responses={status.HTTP_200_OK:
                   openapi.Response('token.key, Type string', EmailAuthTokenSerializer)}
))
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = EmailAuthTokenSerializer
    # obtain_auth_token view explicitly uses JSON requests and responses,
    # rather than using default renderer and parser classes in your settings, link below.
    # https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    # @swagger_auto_schema(request_body=EmailAuthTokenSerializer(),responses={200: 'Token'})
    def post(self, request, *args, **kwargs):
        response = super(CreateTokenView, self).post(request, *args, **kwargs)
        return Response(data=response.data, status=response.status_code)
