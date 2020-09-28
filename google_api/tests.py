from django.contrib.sites.models import Site
from django.test import TestCase, Client
from django.urls import reverse
from social.models import SocialProvider

call_back_url_names = ['google_callback_signup', 'google_callback_login', 'google_callback_login_signup',
                       'google_callback_add_social', 'google_callback_revoke', ]

ajax_call_back_url_names = ['google_ajax_signup', 'google_ajax_login', 'google_ajax_add_social', ]


class TestGoogleCallbacks(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_csrf = Client(enforce_csrf_checks=True)

        self.userId = 'AC8'
        self.email = 'test@gmail.com'
        self.is_email_verified = True

        self.userId_2 = 'AC9'
        self.email_2 = 'test2@gmail.com'
        self.is_email_verified_2 = False

    def test_google_api_callback(self):
        for call in call_back_url_names:
            response = self.client.get(reverse('google_call', kwargs={'google_caller_url_name': call}))
            self.assertEqual(response.status_code, 302)

    def test_google_api_ajax_callback(self):
        # client_id is used in the template context
        SocialProvider(social=SocialProvider.GOOGLE, client_id='1234567891011121314151617181920').save()
        for call in ajax_call_back_url_names:
            response = self.client.get(reverse('google_ajax', kwargs={'google_ajax_url_name': call}))
            self.assertEqual(response.status_code, 200)

    def test_google_api_ajax_force_csrf(self):
        """test Whether CSRF cookie is send without any csrf tag"""
        SocialProvider(social=SocialProvider.GOOGLE, client_id='1234567891011121314151617181920').save()
        for call in ajax_call_back_url_names:
            response = self.client_csrf.get(reverse('google_ajax', kwargs={'google_ajax_url_name': call}))
            self.assertNotContains(response, 'csrfmiddlewaretoken')  # there is no csrf_token tag
            self.assertIsNotNone(response.cookies.get('csrftoken', None))  # csrf_token cookie is set
