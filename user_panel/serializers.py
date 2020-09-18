from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }