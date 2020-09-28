from django.contrib.sites.models import Site
from django.test import TestCase, Client

from social.models import SocialProvider, SocialAccount


class TestSocial(TestCase):
    def setUp(self):
        self.client = Client()

        self.userId = 'AC8'
        self.email = 'test@gmail.com'
        self.is_email_verified = True

        self.userId_2 = 'AC9'
        self.email_2 = 'test2@gmail.com'
        self.is_email_verified_2 = False

        SocialProvider(social=SocialProvider.GOOGLE, client_id='1234567891011121314151617181920').save()
        SocialProvider(social=SocialProvider.GITHUB, client_id='ACD1254654AS').save()

    def test_create_social(self):
        """Test sign up with social account"""
        socialAccount = SocialAccount.objects.filter(
            social_provider_identifier=self.userId,
            provider=SocialProvider.objects.get(social=SocialProvider.GOOGLE),
            site=Site.objects.get_current())
        account_count = socialAccount.count()
        # if the google id has an account log in the user
        if account_count == 1:
            # there should be only one result back
            socialAccount = socialAccount[0]
        elif account_count == 0:
            try:
                from social.views import create_social_create_email_user
                emailUser, socialAccount = create_social_create_email_user(
                    self.userId, self.email,
                    SocialProvider.objects.get(
                        social=SocialProvider.GOOGLE),
                    self.is_email_verified)
            except ValueError:
                pass
        else:
            """this is unexpected"""
            # server error occur now

        # log in the account
        self.client.force_login(socialAccount.user)

        self.assertEqual(socialAccount.email, self.email)
        self.assertEqual(socialAccount.social_provider_identifier, self.userId)
        self.assertEqual(socialAccount.site, Site.objects.get_current())
        self.assertEqual(socialAccount.provider.social, SocialProvider.GOOGLE)
        self.assertTrue(socialAccount.is_connected)
        self.assertEqual(socialAccount.user.is_email_verified, self.is_email_verified)
        self.assertTrue(socialAccount.user.is_authenticated)

    def test_login_by_social(self):
        """Test sign in a user with social account"""
        from social.views import create_social_create_email_user
        _, socialAccount = create_social_create_email_user(self.userId, self.email,
                                                           SocialProvider.objects.get(
                                                               social=SocialProvider.GOOGLE),
                                                           self.is_email_verified)

        socialAccount = SocialAccount.objects.filter(
            social_provider_identifier=self.userId,
            provider=SocialProvider.objects.get(social=SocialProvider.GOOGLE),
            site=Site.objects.get_current())
        account_count = socialAccount.count()

        # if the google id has an account log in the user
        if account_count == 1:
            # there should be only one result back
            socialAccount = socialAccount[0]
        elif account_count == 0:
            try:
                from social.views import create_social_create_email_user
                _, socialAccount = create_social_create_email_user(
                    self.userId, self.email,
                    SocialProvider.objects.get(
                        social=SocialProvider.GOOGLE),
                    self.is_email_verified)
            except ValueError:
                pass
        else:
            """this is unexpected"""
            # server error occur now

        # log in the account
        self.client.force_login(socialAccount.user)

        self.assertEqual(socialAccount.email, self.email)
        self.assertEqual(socialAccount.social_provider_identifier, self.userId)
        self.assertEqual(socialAccount.site, Site.objects.get_current())
        self.assertEqual(socialAccount.provider.social, SocialProvider.GOOGLE)
        self.assertTrue(socialAccount.is_connected)
        self.assertEqual(socialAccount.user.is_email_verified, self.is_email_verified)
        self.assertTrue(socialAccount.user.is_authenticated)

    def test_delete_provider(self):
        """test that after a provider account deleted SocialAccounts must remain with their provider field == 'sentinel'
        while other SocialAccounts must remain intact"""
        from social.views import create_social_create_email_user
        _, socialAccount_1 = create_social_create_email_user(
            self.userId,
            self.email,
            SocialProvider.objects.get(social=SocialProvider.GOOGLE),
            self.is_email_verified)

        _, socialAccount_2 = create_social_create_email_user(
            self.userId_2, self.email_2,
            SocialProvider.objects.get(social=SocialProvider.GITHUB),
            self.is_email_verified)

        self.assertEqual(socialAccount_1.provider.social, SocialProvider.GOOGLE)
        self.assertEqual(socialAccount_2.provider.social, SocialProvider.GITHUB)

        SocialProvider.objects.get(social=SocialProvider.GOOGLE).delete()

        socialAccount_1.refresh_from_db()
        socialAccount_2.refresh_from_db()
        self.assertEqual(socialAccount_1.provider.social, SocialProvider.SENTINEL)
        self.assertEqual(socialAccount_2.provider.social, SocialProvider.GITHUB)
