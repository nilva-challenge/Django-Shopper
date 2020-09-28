from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from social.models import SocialProvider
from google_token_util import authorize_by_google_api_profile

UserModel = get_user_model()


class GoogleTokenSerializer(serializers.Serializer):
    """Serializer for google javascript client"""

    id_token = serializers.CharField(
        label=_("google ID token"),
        trim_whitespace=False,
        required=True,
        write_only=True,
        min_length=3,
        help_text=_("google javascript Client token and information"),
    )
    error_messages = {
        'third_party_authorization_fail': _('Authorization failed by third party: Google javascript client.'),
    }

    # class Meta:
    #     fields = ('id_token',)

    def validate_id_token(self, id_token):
        """
        Check id token by google, then extract user information
        """
        idinfo = authorize_by_google_api_profile(SocialProvider.objects.get(social=SocialProvider.GOOGLE).client_id,
                                                 id_token)

        if idinfo is None:
            raise serializers.ValidationError("Token is not valid")

        return idinfo

    # def create(self, validated_data):
    #     pass
    #
    # def update(self, instance, validated_data):
    #     pass
