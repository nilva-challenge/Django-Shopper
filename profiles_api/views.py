from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User
from rest_framework_jwt.serializers import jwt_payload_handler
from django.contrib.auth.signals import user_logged_in
from rest_framework.response import Response
from rest_framework import status
import jwt
from django_shopper import settings
from .serializers import UserProfileSerializer
from .permissions import IsOwner, IsSuperUser
from rest_framework import viewsets
from rest_framework import filters
from django_shopper.messages import success, errors
from django.contrib.auth import authenticate


@api_view(['POST'])  # this method  works with post
@permission_classes([AllowAny, ])  # any body can access to this method
def authenticate_user(request):
    """Create token for next steps(Login)"""
    try:
        email = request.data['email']
        password = request.data['password']
        if email == '' or password == '':  # validate
            code = 100
            error = {
                'code': code,
                'msg': errors[code]
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)
        user_authenticate = authenticate(email=email, password=password)  # check if user there is in database
        if user_authenticate is not None:
            try:
                payload = jwt_payload_handler(user_authenticate)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['id'] = user_authenticate.id
                user_details['user'] = user_authenticate.email
                user_details['token'] = token
                user_logged_in.send(sender=user_authenticate.__class__, request=request, user=user_authenticate)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:  # if email user there is not in database,it will be created..
            if len(User.objects.filter(email=email)) > 0:
                code = 105
                error = {
                    'code': code,
                    'msg': errors[code]
                }
                return Response(error, status.HTTP_400_BAD_REQUEST)
            else:
                result = create_user(request)
                if result == 1:
                    code = 201
                    success_msg = {
                        'code': code,
                        'msg': success[code]
                    }
                    return Response(success_msg, status=status.HTTP_201_CREATED)
                elif result == 2:
                    code = 105
                    error = {
                        'code': code,
                        'msg': errors[code]
                    }
                    return Response(error, status.HTTP_400_BAD_REQUEST)
                else:
                    code = 104
                    error = {
                        'code': code,
                        'msg': errors[code]
                    }
                    return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except KeyError:
        code = 104
        error = {
            'code': code,
            'msg': errors[code]
        }
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny, ])  # any body can access to this method
def create_user(request):
    """method for register that  is called in auth_token method"""
    try:
        serializer_class = UserProfileSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            User.objects.create_user(email=email, password=password)
            return 1
        else:
            return 2  # is not valid email or password

    except:
        return 0


class UserProfileViewSet(viewsets.ModelViewSet):
    """create user profile and update profile"""
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_permissions(self):  # this method is for define user permission for updating own profile
        if self.action == 'list':
            self.permission_classes = [IsSuperUser, ]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner]
        return super(self.__class__, self).get_permissions()

    filter_backends = (filters.SearchFilter,)  # in browser there is filter base on name and email in list ,and admin user has permission to see list of product
    search_fields = ('name', 'email',)
