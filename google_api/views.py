import sys
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.models import Site
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.db import DatabaseError
from rest_framework.authtoken.models import Token
from google_api.serializers import GoogleTokenSerializer
from social.models import SocialAccount, SocialProvider
from .google_token_util import authorize_by_google_api_profile

USER_MODEL = get_user_model()
if hasattr(settings, 'GOOGLE_CLIENT_FILE_PATH'):
    GOOGLE_CLIENT_FILE_PATH = settings.GOOGLE_CLIENT_FILE_PATH
else:
    raise ValueError('GOOGLE_CLIENT_FILE_PATH is required in settings')

SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', ]

# view names that require logged in user
REQUIRE_LOGGED_IN_URL_NAMES = ['google_callback_add_social', 'google_callback_revoke']


# GOOGLE_OPTIONS = None

@require_http_methods(["GET", ])
def google_call(request, google_caller_url_name):
    """
    :param request:
    :param google_caller_url_name: str
        name of the url to get called-back by google.
    """
    # view names that require logged in user
    if google_caller_url_name in REQUIRE_LOGGED_IN_URL_NAMES:
        # view require logged in user
        if not request.user.is_authenticated:
            return redirect_to_login(request.path, login_url=reverse('user:login'))
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    import google_auth_oauthlib.flow
    flow = None
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(GOOGLE_CLIENT_FILE_PATH, SCOPES, )
    except ValueError as err:
        print(err)
        return redirect('google_error')
    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    try:
        # todo any better idea to make the url?
        flow.redirect_uri = '%s%s' % (request.build_absolute_uri('/')[:-1], reverse(google_caller_url_name))
    except KeyError:
        return redirect('google_error')

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    # Enable incremental authorization. Recommended as a best practice.
    # include_granted_scopes = 'true',
    # login_hint=request.user.is_anonymous or request.user.email,
    # re-prompting the user for permission. Recommended for web server apps.
    # prompt='consent',
    # Enable offline access so that you can refresh an access token without
    # access_type = 'offline',
    GOOGLE_OPTIONS = None
    if hasattr(settings, 'GOOGLE_OPTIONS'):
        GOOGLE_OPTIONS = settings.GOOGLE_OPTIONS
    authorization_url, state = flow.authorization_url(**GOOGLE_OPTIONS)

    return redirect(authorization_url)


@require_http_methods(["GET", ])
@user_passes_test(lambda u: u.is_anonymous, login_url=reverse_lazy('google'), redirect_field_name=None)
def google_callback_signup(request):
    from social.views import create_social_create_email_user

    if 'access_denied' == request.GET.get('error', ''):
        return redirect('google_error')

    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    redirect_uri = request.GET.get('redirect_uri', request.build_absolute_uri('?'))
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_FILE_PATH,
        SCOPES,
        state=state)
    flow.redirect_uri = redirect_uri
    try:
        flow.fetch_token(code=code)
    except Exception as err:
        print("google_callback_signup: ", err)
        print("Unexpected error: ", sys.exc_info()[0])
        return redirect('google_error')

    # obligates https
    # authorization_response = request.build_absolute_uri()
    # flow.fetch_token(authorization_response=authorization_response)

    try:
        idinfo = authorize_by_google_api_profile(flow.credentials.client_id, flow.credentials.id_token, )
        userId = idinfo['sub']
        email = idinfo['email']
        isEmailVerified = idinfo['email_verified']
    except ValueError as err:
        print('google_callback_signup: ', err)
        return redirect('google_error')

    try:
        create_social_create_email_user(userId, email, SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                        isEmailVerified)
    except ValueError as err:
        print(err)
        return redirect('google_error')

    return redirect('google')


@require_http_methods(["GET", ])
@user_passes_test(lambda u: u.is_anonymous, login_url=reverse_lazy('google'), redirect_field_name=None)
def google_callback_login(request):
    if 'access_denied' == request.GET.get('error', ''):
        return redirect('google_error')

    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    redirect_uri = request.GET.get('redirect_uri', request.build_absolute_uri('?'))
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_FILE_PATH,
        SCOPES,
        state=state)
    flow.redirect_uri = redirect_uri
    try:
        flow.fetch_token(code=code)
    except Exception as err:
        print("Exception:", err)
        return redirect('google_error')

    # obligates https
    # authorization_response = request.build_absolute_uri()
    # flow.fetch_token(authorization_response=authorization_response)
    idinfo = authorize_by_google_api_profile(flow.credentials.client_id, flow.credentials.id_token, )
    userId = idinfo['sub']
    try:
        account = SocialAccount.objects.get(social_id=userId,
                                            provider=SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                            site=Site.objects.get_current())
    except SocialAccount.DoesNotExist:
        # there is no user with this social account by the given google user id
        return redirect('google_error')

    # LogIn the user with the social account
    login(request, account.user, )

    return redirect('google', )


@require_http_methods(["GET", ])
@user_passes_test(lambda u: u.is_anonymous, login_url=reverse_lazy('google'), redirect_field_name=None)
def google_callback_login_signup(request):
    """
    @param request:
    @return:

    if Google id is associated with a user log in the user
    if Google id is NOT associated with a user make the user and social account then  log in the user
    """
    if 'access_denied' == request.GET.get('error', ''):
        return redirect('google_error')

    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    redirect_uri = request.GET.get('redirect_uri', request.build_absolute_uri('?'))
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_FILE_PATH,
        SCOPES,
        state=state)
    flow.redirect_uri = redirect_uri
    try:
        flow.fetch_token(code=code)
    except Exception as err:
        print("Exception:", err)
        return redirect('google_error')

    try:
        idinfo = authorize_by_google_api_profile(flow.credentials.client_id, flow.credentials.id_token, )
        userId = idinfo['sub']
        email = idinfo['email']
        isEmailVerified = idinfo['email_verified']
    except ValueError as err:
        print('google_callback_signup: ', err)
        return redirect('google_error')

    account = SocialAccount.objects.filter(social_id=userId,
                                           provider=SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                           site=Site.objects.get_current())

    # if the google id has an account log in the user
    if account:
        # there should be only one result back
        account = account[0]
        # LogIn the user with the social account
        login(request, account.user, )
        return redirect('google', )
    else:
        try:
            from social.views import create_social_create_email_user
            create_social_create_email_user(userId, email, SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                            isEmailVerified)
        except ValueError as err:
            print('google_callback_login_signup', err)
            return redirect('google_error')

        account = SocialAccount.objects.get(social_id=userId,
                                            provider=SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                            site=Site.objects.get_current())
        login(request, account.user, )

        return redirect('google', )


@require_http_methods(["GET", ])
@login_required(login_url=reverse_lazy('user:login'), redirect_field_name=None)
def google_callback_add_social(request):
    if 'access_denied' == request.GET.get('error', ''):
        return redirect('google_error')

    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    redirect_uri = request.GET.get('redirect_uri', request.build_absolute_uri('?'))
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_FILE_PATH,
        SCOPES,
        state=state)
    flow.redirect_uri = redirect_uri
    try:
        flow.fetch_token(code=code)
    except ValueError as err:
        print("flow.fetch_token: ", err)
        return redirect('google_error')
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        return redirect('google_error')

    # authorization_response = request.build_absolute_uri()
    # obligates https
    # flow.fetch_token(authorization_response=authorization_response)

    idinfo = authorize_by_google_api_profile(flow.credentials.client_id, flow.credentials.id_token, )
    social_id = idinfo['sub']
    email = idinfo['email']
    # is_email_verified = idinfo['email_verified']
    try:
        socialAccount, isCreated = SocialAccount.objects.get_or_create(site=Site.objects.get_current(),
                                                                       user=request.user,
                                                                       provider=SocialProvider.objects.get(
                                                                           social=SocialProvider.GOOGLE),
                                                                       defaults={
                                                                           'social_provider_identifier': social_id,
                                                                           'is_connected': True,
                                                                           'email': email, })

    except DatabaseError:
        # database error
        return redirect('google_error')
    if isCreated:
        # social account created and added to the user
        return redirect('google')
    else:
        # social account already exist for the user
        return redirect('google_error')


@require_http_methods(["GET", ])
@login_required(login_url=reverse_lazy('user:login'), redirect_field_name=None)
def google_callback_revoke(request):
    if 'access_denied' == request.GET.get('error', ''):
        return redirect('google_error')

    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    redirect_uri = request.GET.get('redirect_uri', request.build_absolute_uri('?'))
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_FILE_PATH,
        SCOPES,
        state=state)
    flow.redirect_uri = redirect_uri
    try:
        flow.fetch_token(code=code)
    except Exception as err:
        print("google_callback_revoke: ", err)
        print("Unexpected error:", sys.exc_info()[0])
        return redirect('google_error')

    import requests
    requests.post('https://accounts.google.com/o/oauth2/revoke',
                  params={'token': flow.credentials.token},
                  headers={'content-type': 'application/x-www-form-urlencoded'})
    return redirect('google')


"""
the following is used by the javascript version of the google api
"""


@method_decorator(ensure_csrf_cookie, name='dispatch')
class TemplateCSRFView(TemplateView):
    """
    this view always sends csrf token with response
    (means there is no need for {% csrf token %} (tag) in template to get the csrf token)
    """
    """
    A view for loading google javascript api and ajax json post by xhr
    """
    template_name = 'google_api/google_api.html'

    # add client_id to context data to use in template
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'client_id' not in data:
            data['client_id'] = SocialProvider.objects.get(social=SocialProvider.GOOGLE).client_id

        return data


class JsonGoogleAjaxMixin:
    """
    Mixin for AJAX support json.

    request.is_ajax()
    https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.is_ajax
    Returns True if the request was made via an XMLHttpRequest, by checking the HTTP_X_REQUESTED_WITH header for the string 'XMLHttpRequest'
    """
    id_token = None

    # We make sure to call the parent's form_valid() method because
    # it might do some processing (in the case of CreateView, it will
    # call form.save() for example).
    def get_id_token(self, request):
        from django.http import JsonResponse
        if request.is_ajax():  # HTTP_X_REQUESTED_WITH == 'XMLHttpRequest'
            import json
            self.id_token = json.loads(request.body).get('id_token', None)
            if self.id_token:
                return True
            else:
                return JsonResponse({'status': 'false', 'error': 'denied by google'}, status=400)
        else:
            return JsonResponse({'status': 'false', 'error': 'not ajax'}, status=400)


class GoogleAuthorizeAjaxMixin(JsonGoogleAjaxMixin):
    idinfo = None

    def get_id_info(self, request):
        if super().get_id_token(request):
            # authenticate google id_token
            # google id_token is valid go to index page
            self.idinfo = authorize_by_google_api_profile(
                SocialProvider.objects.get(social=SocialProvider.GOOGLE).client_id, self.id_token)
            return True

        # authentication failed
        from django.http import JsonResponse
        return JsonResponse({'status': 'false', 'error': 'denied by google'}, status=400)


decorators = [require_http_methods(["POST", ]),
              user_passes_test(lambda u: u.is_anonymous, login_url=reverse_lazy('google'),
                               redirect_field_name=None), ]


@method_decorator(decorators, name='dispatch')
class GoogleSignupAjaxView(GoogleAuthorizeAjaxMixin, View):

    def post(self, request):
        if super().get_id_info(request):
            userId = self.idinfo.get('sub', None)
            email = self.idinfo.get('email', None)
            isEmailVerified = self.idinfo.get('email_verified', None)
            try:
                from social.views import create_social_create_email_user
                create_social_create_email_user(userId, email,
                                                SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                                isEmailVerified)
            except ValueError as err:
                print(err)
                return JsonResponse({'status': 'false', 'error': 'already exist'}, status=400)
        else:
            return JsonResponse({'status': 'false', 'error': 'denied by google'}, status=400)
        return JsonResponse({'status': 'ok', }, status=200)


decorators = [require_http_methods(["POST", ])]


@method_decorator(decorators, name='dispatch')
class GoogleAjaxLoginView(GoogleAuthorizeAjaxMixin, View):
    def post(self, request):
        if super().get_id_info(request):
            userId = self.idinfo.get('sub', None)
            try:
                account = SocialAccount.objects.get(social_id=userId,
                                                    provider=SocialProvider.objects.get(
                                                        social=SocialProvider.GOOGLE),
                                                    site=Site.objects.get_current())
            except SocialAccount.DoesNotExist:
                # there is no user with this social account by the given google user id
                return JsonResponse({'status': 'false', 'error': 'account not found'}, status=400)

            # LogIn the user with the social account
            login(request, account.user, )

            return JsonResponse({'status': 'ok'}, status=200)


decorators = [require_http_methods(["POST", ]),
              login_required(login_url=reverse_lazy('user:login'), )]


@method_decorator(decorators, name='dispatch')
class GoogleAjaxAddSocialView(GoogleAuthorizeAjaxMixin, View):

    def post(self, request):
        if super().get_id_info(request):
            userId = self.idinfo.get('sub', None)
            email = self.idinfo.get('email', None)
            isEmailVerified = self.idinfo.get('email_verified', None)

            try:
                socialAccount, isCreated = SocialAccount.objects.get_or_create(site=Site.objects.get_current(),
                                                                               user=request.user,
                                                                               provider=SocialProvider.objects.get(
                                                                                   social=SocialProvider.GOOGLE),
                                                                               defaults={
                                                                                   'social_provider_identifier': userId,
                                                                                   'is_connected': True,
                                                                                   'email': email, })
            except DatabaseError as err:
                # database error
                print('GoogleAjaxAddSocial', err)
                return JsonResponse({'status': 'false', 'error': ''}, status=400)

            if isCreated:
                # social account created and added to the user
                return JsonResponse({'status': 'ok'}, status=200)
            else:
                # social account already exist for the user
                return JsonResponse({'status': 'false', 'error': 'account exist'}, status=400)


class GoogleLoginSignupConnectAjaxView(GoogleAuthorizeAjaxMixin, View):
    """
    these happen in order
    login if user exists with the social account,
    if user is already authenticated, add social to the user
    if user with social email exists and the email verified, add social to the user
    if not, create and login the user


    user must be anonymous otherwise redirect to logout
    """

    def post(self, request):
        if super().get_id_info(request) is not None:
            user_id = self.idinfo.get('sub', None)
            email = self.idinfo.get('email', None)
            is_email_verified = self.idinfo.get('email_verified', False)

            try:
                if SocialAccount.objects.filter(
                        social_provider_identifier=user_id,
                        provider=SocialProvider.objects.get(
                            social=SocialProvider.GOOGLE),
                        site=Site.objects.get_current()).exists():
                    # log in the user associated with social account
                    user = SocialAccount.objects.get(
                        social_provider_identifier=user_id,
                        provider=SocialProvider.objects.get(
                            social=SocialProvider.GOOGLE),
                        site=Site.objects.get_current()).user

                    # login the user
                    login(request, user)
                    return JsonResponse({'status': True, 'error': None}, status=200)

                else:
                    # there is no social account for the user from this provider for the current site
                    # from user.models import EmailUser
                    from social.views import add_social_account_to_user, create_social_create_email_user

                    # if user is authenticated just connect the user to the social account
                    if request.user.is_authenticated:
                        add_social_account_to_user(request.user, social_id=user_id, email=email)

                        return JsonResponse({'status': True, 'error': None}, status=201)

                    # if user is not authenticated but have email like the one trying to associate with,
                    # and email is verified, then associate them, it's more secure to ask for password for the action
                    elif USER_MODEL.objects.filter(email=email, site=Site.objects.get_current(),
                                                   is_email_verified=True).exists():

                        user = USER_MODEL.objects.get(email=email, site=Site.objects.get_current(),
                                                      is_email_verified=True)
                        add_social_account_to_user(user=user, social_id=user_id, email=email)

                        login(request, user)
                        return JsonResponse({'status': True, 'error': None}, status=201)

                    # no user exists for the social account, user is not authenticated
                    else:
                        create_social_create_email_user(user_id, email,
                                                        SocialProvider.objects.get(social=SocialProvider.GOOGLE),
                                                        is_email_verified)

                        return JsonResponse({'status': True, 'error': None}, status=201)

            except DatabaseError as err:
                # database error
                print('GoogleAjaxAddSocial:', err)
                return JsonResponse({'status': 'false', 'error': ''}, status=500)


# django rest framework
class JsonGoogleRESTMixin:
    """
    Mixin for REST API support.
    """
    id_token = None

    def get_id_token(self, request):
        from django.http import JsonResponse
        if request.is_ajax():  # HTTP_X_REQUESTED_WITH == 'XMLHttpRequest'
            import json
            self.id_token = json.loads(request.body).get('id_token', None)
            if self.id_token:
                return True
            else:
                return JsonResponse({'status': 'false', 'error': 'denied by google'}, status=400)
        else:
            return JsonResponse({'status': 'false', 'error': 'not ajax'}, status=400)


class GoogleAuthorizeRESTMixin(JsonGoogleRESTMixin):
    idinfo = None

    def get_id_info(self, request):
        if super().get_id_token(request):
            # authenticate google id_token
            # google id_token is valid go to index page
            self.idinfo = authorize_by_google_api_profile(
                SocialProvider.objects.get(social=SocialProvider.GOOGLE).client_id, self.id_token)
            return True

        # authentication failed
        from django.http import JsonResponse
        return JsonResponse({'status': 'false', 'error': 'denied by google'}, status=400)


from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, status


class GoogleLoginSignupConnectRESTView(GenericAPIView):
    """
    these happen in order
    login if user exists with the social account,
    if user is already authenticated, add social to the user
    if user with social email exists and the email verified, add social to the user
    if not, create and login the user
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []
    serializer_class = GoogleTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_third_party_association(request, serializer)

    def perform_third_party_association(self, request, serializer):
        idinfo = serializer.validated_data['id_token']
        user_id = idinfo.get('sub', None)
        email = idinfo.get('email', None)
        is_email_verified = idinfo.get('email_verified', False)

        try:
            if SocialAccount.objects.filter(
                    social_provider_identifier=user_id,
                    provider=SocialProvider.objects.get(
                        social=SocialProvider.GOOGLE),
                    site=Site.objects.get_current()).exists():
                # log in the user associated with social account
                user = SocialAccount.objects.get(
                    social_provider_identifier=user_id,
                    provider=SocialProvider.objects.get(
                        social=SocialProvider.GOOGLE),
                    site=Site.objects.get_current()).user

                # send Token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

            else:
                # there is no social account for the user from this provider for the current site
                # from user.models import EmailUser
                from social.views import add_social_account_to_user, create_social_create_email_user

                # if user is authenticated just connect the user to the social account
                if request.user.is_authenticated:
                    add_social_account_to_user(request.user, social_id=user_id, email=email)
                    return Response({'token': 'you already have token!'}, status=status.HTTP_201_CREATED)

                # if user is not authenticated but have email like the one trying to associate with,
                # and email is verified, then associate them, it's more secure to ask for password for the action
                elif USER_MODEL.objects.filter(email=email, site=Site.objects.get_current(),
                                               is_email_verified=True).exists():

                    user = USER_MODEL.objects.get(email=email, site=Site.objects.get_current(),
                                                  is_email_verified=True)
                    add_social_account_to_user(user=user, social_id=user_id, email=email)

                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

                # no user exists for the social account, user is NOT authenticated
                else:
                    user, social_account = create_social_create_email_user(user_id, email,
                                                                           SocialProvider.objects.get(
                                                                               social=SocialProvider.GOOGLE),
                                                                           is_email_verified)

                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        except DatabaseError as err:
            # database error
            print('GoogleAjaxAddSocial:', err)
            return JsonResponse({'status': 'false', 'error': ''}, status=500)
