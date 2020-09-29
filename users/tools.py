import re
from django.core import serializers
from django.utils.crypto import get_random_string
from users.models import Token


def createtoken():
    this_token = get_random_string(length=100)
    try:
        Token.objects.get(key=this_token)
        return createtoken()
    except Token.DoesNotExist:
        Token.objects.create(key=this_token)
        return this_token


def checktokenlogedin(token):
    if token.user == "" or token.user is None:
        return False
    else:
        return True
