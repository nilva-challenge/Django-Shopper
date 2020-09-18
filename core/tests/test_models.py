from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "mr.amirhossein1836@gmail.com"
        password = "Pass.123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """Test user email is normalized"""
        email = 'mr.amirhossein1836@GMAIL.com'
        user = get_user_model().objects.create_user(
            email=email,
            password="Pass.123"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Pass.123')

    def test_create_new_superuser(self):
        """Test creating new super user"""
        user = get_user_model().objects.create_superuser(
            email='mr.amirhossein1836@gmail.com',
            password='Pass.123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
