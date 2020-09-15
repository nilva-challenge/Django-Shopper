from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from accounts.serializers import UserSerializer, ProfileSerializer
from rest_framework.authtoken.models import Token


class UserAPI(APIView):
    """
    Creates or log in the User
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Creates the token if user doesnt exists in data base
                # get the token if user exists in database
                token = Token.objects.get_or_create(user=user)
                response = {'token': token[0].key}
                # Returns token of authenticated user as Response
                return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.RetrieveUpdateAPIView, CreateModelMixin):
    """
    Returns the Profile if method is GET
    Edits the Profile if method is PUT
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
