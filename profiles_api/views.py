from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import UserProfile
from rest_framework_jwt.serializers import jwt_payload_handler
from django.contrib.auth.signals import user_logged_in
from rest_framework.response import Response
from rest_framework import status
import jwt
from django_shopper import settings
from .serializers import UserProfileSerializer

from django.contrib.auth.hashers import make_password


@api_view(['POST'])  # this method  works with post
@permission_classes([AllowAny, ])  # any body can access to this method
def authenticate_user(request):
    """Create token for next steps(Login)"""
    try:
        email = request.data['email']
        password = request.data['password']
        if email == '' or password == '':
            res = {'خطا': 'ایمیل و پسورد نمی توانند خالی باشند.'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)

        user = UserProfile.objects.filter(email=email)
        if user.exists():
            if user[0].check_password(password):
                user = user[0]
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['user'] = user.email
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {'خطا': 'ایمیل و پسورد را صحیح وارد کنید.'}
                return Response(res)
        else:
            result = create_user(request)

            if result == 1:
                res = {'پیغام': 'ثبت نام شما با موفقیت انجام شد.'}
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {'پیغام': 'با خطا مواجه شده اید.'}
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except KeyError:
        res = {'خطا': 'افزودن فیلد های ایمیل و پسورد اجباری می باشند.'}
        return Response(res)


@permission_classes([AllowAny, ])  # any body can access to this method
def create_user(request):
    try:
        serializer_class = UserProfileSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            UserProfile.objects.create_user(email=email, password=(password))
            return 1
    except:
        return 0
