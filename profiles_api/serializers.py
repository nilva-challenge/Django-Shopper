from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializers a user profile object"""

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }},  # when read dont show password
            # 'email': {
            #     'read_only': True,  # do not permit to change email
            #
            # }
        }  # convert model instance into python object with serializer
