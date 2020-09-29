from functools import wraps
from json import JSONEncoder

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from users.models import Token, User


def token_required(func):
    @wraps(func)
    def wrap(request, **kwargs):
        token = request.META.get('HTTP_TOKEN', None)
        # print(request.META)
        if token:
            try:
                token_obj = Token.objects.get(key=token)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {'status': 'error',
                     'type': 'YourTokenDoesNotExist',
                     }, encoder=JSONEncoder, status=401)
            kwargs['token'] = token_obj
        elif token is None or token == '':
            return JsonResponse(
                {'status': 'error',
                 'type': 'TokenHeaderDoesNotExist',
                 }, encoder=JSONEncoder, status=400)
        result = func(request, **kwargs)
        return result
    return wrap


def user_required(func):
        @wraps(func)
        @token_required
        def wrap(request, token, **kwargs):
            try:
                # kwargs['token'] = token
                kwargs['user'] = User.objects.get(token=token)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {'status': 'error',
                     'type': 'YourUserDoesNotExist',
                     }, encoder=JSONEncoder, status=401)
            result = func(request, **kwargs)
            return result
        return wrap


