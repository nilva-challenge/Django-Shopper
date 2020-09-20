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


class UserEditSerializer(serializers.ModelSerializer):
    """Serailizer for edit user model"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'password',
            'name',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }

    def update(self, instance, validated_data):
        """Update the user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
