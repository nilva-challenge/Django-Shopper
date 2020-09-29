from django.views.decorators.http import require_POST, require_GET
import json
from .models import User, Token
from users import tools
from django.core.exceptions import *
from json import JSONEncoder
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import requests

# login or signup by email
@require_GET
def login_with_email(request):
    if 'email' in request.GET and 'password' in request.GET:
        password = request.GET['password']
        email = request.GET['email']

        if User.objects.filter(email=email).exists():

            this_user = User.objects.get(email=email)
            if (check_password(password, this_user.password)):
                created_token = tools.createtoken()
                main_token = Token.objects.get(key=created_token)
                main_token.user = this_user
                main_token.save()
                return JsonResponse({
                    'status': 'ok',
                    'token': main_token.key,
                    'text': 'ورود موفق'
                }, encoder=JSONEncoder)

            else:
                context = {}
                context['status'] = 'error'
                context['type'] = 'PasswordIsWrong'
                return JsonResponse(context, encoder=JSONEncoder, status=403)
        else:
            this_user = User.objects.create_user(email=email, password=password)
            created_token = tools.createtoken()
            main_token = Token.objects.get(key=created_token)
            main_token.user = this_user
            main_token.save()
            return JsonResponse({
                'status': 'ok',
                'token': main_token.key,
                'text': 'ورود موفق'
            }, encoder=JSONEncoder)
    else:
        return JsonResponse({'status': 'error',
                             'type': 'EmailAndPasswordMustBeSet'}, status=403)

# login or signup with google
@require_GET
def sign_in_with_google(request):
    if 'id_token' in request.GET:
        id_token = request.GET.get('id_token')

        url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + id_token

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        body = json.loads(response.text)
        if User.objects.filter(email=body["email"]).exists():
            this_user = User.objects.get(email=body["email"])
        else:
            password = User.objects.make_random_password()
            this_user = User.objects.create_user(email=body["email"], password=password)
        created_token = tools.createtoken()
        main_token = Token.objects.get(key=created_token)
        main_token.user = this_user
        main_token.save()
        return JsonResponse({
            'status': 'ok',
            # 'phone_number': this_user.phone_number,
            'token': main_token.key,
            'text': 'ورود موفق'
        }, encoder=JSONEncoder)

    else:
        return JsonResponse({'status': 'error',
                             'type': 'ID_TokenMustBeSet'}, status=403)


from DjangoShopper.decorators import token_required

# get profile info
@token_required
def get_my_profile(request, token):
    user = User.objects.values("first_name", "last_name", "email", "address", "postal_code").get(token=token)
    return JsonResponse(user, safe=False)


from django.views.decorators.csrf import csrf_exempt

# update profile info
@token_required
@csrf_exempt
def update_my_profile(request, token):
    user = User.objects.get(token=token)

    if 'first_name' in request.POST:
        user.first_name = request.POST["first_name"]
    if 'last_name' in request.POST:
        user.last_name = request.POST["last_name"]

    if 'address' in request.POST:
        user.address = request.POST["address"]

    if 'postal_code' in request.POST:
        user.postal_code = request.POST["postal_code"]

    if 'password' in request.POST:
        user.password = make_password(request.POST["password"])
    user.save()
    return JsonResponse({
        'status': 'ok',

    }, encoder=JSONEncoder)