from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class EmailUserSerializer(serializers.ModelSerializer):
    """Base serializer for email user"""
    password = serializers.CharField(
        label=_("Password"),
        trim_whitespace=False,
        required=False,
        write_only=True,
        min_length=8,
        help_text=_("Enter the password for your account."),
    )

    email = serializers.EmailField(label='Email', max_length=254, required=True,
                                   validators=[UniqueValidator(queryset=UserModel.objects.all(),
                                                               message='Unable to sign in with provided credentials.')])

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'min_length': 8}, }

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        password = validated_data.pop('password', None)
        return UserModel.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        """ Update a user, setting the password correctly and return it """

        # get rid of security data as soon as possible, here we pop password
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class DynamicFieldsModelSerializer(EmailUserSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        fields_extra_kwargs = kwargs.pop('fields_extra_kwargs', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            print('allowed:', allowed)
            print('existing:', existing)
            for field_name in existing - allowed:
                print('field will remove:', field_name)
                self.fields.pop(field_name)


class EmailAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(label=_("Email"), min_length=5, style={'input_type': 'email'}, write_only=True)
    token = serializers.CharField(label=_("Token"), style={'input_type': 'password'}, read_only=True)

    class Meta:
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
