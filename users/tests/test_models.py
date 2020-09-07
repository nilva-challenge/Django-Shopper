from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModels(TestCase):

    def test_user_model(self):
        """test creating a user model an get her/his email"""
        email = 'test@me.com'
        password = 'test123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertEqual(str(user), user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
