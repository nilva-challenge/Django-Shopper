from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client

from user.forms import CustomAuthenticationForm, CustomUserCreationForm

LOGIN_URL = reverse('user:login')
SIGNUP_URL = reverse('user:signup')
LOGOUT_URL = reverse('user:logout')
PASSWORD_CHANGE_URL = reverse('user:password_change')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTests(TestCase):
    """Test the users API"""

    def setUp(self):
        self.client = Client()

    def test_login_view_template_name(self):
        """test that correct view and template are used"""
        template_name = 'registration/login.html'
        res = self.client.get(LOGIN_URL)
        self.assertTemplateUsed(res, template_name)
        from user.views import CustomLoginView
        self.assertEqual(res.resolver_match.func.__name__, CustomLoginView.as_view().__name__)

    def test_login_form_html(self):
        """test login template contain log in form"""
        response = self.client.get(LOGIN_URL)

        self.assertContains(response, 'csrfmiddlewaretoken')

        self.assertContains(response, '<input')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, '>')

        self.assertContains(response, '<input')
        self.assertContains(response, 'type="password"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, '>')

    def test_authenticate(self):
        """log in with email and password"""
        credential = {
            'email': 'mahdi',
            'password': 'password',
        }

        create_user(**credential)
        self.assertTrue(self.client.login(**credential))

    def test_login_post(self):
        """test log in via post request"""
        credential = {
            'email': 'mahdi@gmail.com',
            'password': 'password',
        }

        user = create_user(**credential)
        response = self.client.post(LOGIN_URL, data=credential)
        self.assertEqual(response.wsgi_request.user.id, user.id)
        self.assertEqual(response.status_code, 302)

    def test_login_form(self):
        """test CustomAuthenticationForm"""
        credential = {
            'email': "leela@gmail.com",
            'password': "password!",
        }

        user = create_user(**credential)
        form = CustomAuthenticationForm(data=credential)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], credential['email'])
        self.assertEqual(form.cleaned_data['password'], credential['password'])
        self.assertEqual(form.user_cache, user)

    def test_signup_get(self):
        response = self.client.post(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        """test redirect upon successful post"""
        credential = {
            'email': "leela@gmail.com",
            'password1': "ASZX1234!",
            'password2': "ASZX1234!",
        }
        response = self.client.post(SIGNUP_URL, follow=True, data=credential)

        credential = {
            'email': "leela@gmail.com",
            'password': "ASZX1234!",
        }
        self.assertTrue(self.client.login(**credential))

        self.assertEqual(response.redirect_chain[0][0], LOGIN_URL)
        self.assertEqual(response.redirect_chain[0][1], 302)

        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        """test custom user signup form"""
        credential = {
            'email': "leela@gmail.com",
            'password1': "ASZX1234!",
            'password2': "ASZX1234!",
        }
        form = CustomUserCreationForm(data=credential)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        self.assertEqual(form.cleaned_data['email'], credential['email'])
        self.assertEqual(form.cleaned_data['password1'], credential['password1'])
        self.assertEqual(form.cleaned_data['password2'], credential['password2'])
        user_form = form.save()
        user_auth = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password2'])

        # self.assertIsNotNone(user_form)
        self.assertIsNotNone(user_auth)
        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        self.assertIsInstance(user_form, user_model)
        self.assertIsInstance(user_auth, user_model)

        self.assertEqual(user_form.id, user_auth.id, )

    def test_logout(self):
        """test logout view work correctly request response only"""
        credential = {
            'email': "leela@gmail.com",
            'password': "ASZX1234!",
        }
        user = create_user(**credential)
        self.client.force_login(user)
        res = self.client.post(LOGOUT_URL, follow=True)
        self.assertTrue(res.context.request.user.is_anonymous)
        self.assertEqual(res.redirect_chain[0][1], 302)

        self.assertEqual(res.status_code, 200)

    def test_logout_post_only(self):
        """test only POST request is allowed"""
        res = self.client.get(LOGOUT_URL, follow=True)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(LOGOUT_URL, follow=True)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(LOGOUT_URL, follow=True)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(LOGOUT_URL, follow=True)
        self.assertEqual(res.status_code, 405)

        res = self.client.post(LOGOUT_URL, follow=True)
        self.assertEqual(res.redirect_chain[0][1], 302)

    def test_change_password_html(self):
        """test get password change page and password change form """
        credential = {
            'email': "leela@gmail.com",
            'password': "ASZX1234!",
        }
        user = create_user(**credential)
        self.client.force_login(user)

        res = self.client.get(PASSWORD_CHANGE_URL)
        self.assertEqual(res.status_code, 200)

        self.assertContains(res, 'csrfmiddlewaretoken')

        self.assertContains(res, '<input')
        self.assertContains(res, 'name="old_password"')
        self.assertContains(res, '>')

        self.assertContains(res, '<input')
        self.assertContains(res, 'type="password"')
        self.assertContains(res, 'name="new_password1"')
        self.assertContains(res, '>')

        self.assertContains(res, '<input')
        self.assertContains(res, 'type="password"')
        self.assertContains(res, 'name="new_password2"')
        self.assertContains(res, '>')

    def test_change_password_form(self):
        """test password change form"""
        # this form is built in django so we do't test it

    def test_change_password_form_post(self):
        """test password change view by post request"""
        credential = {
            'email': "leela@gmail.com",
            'password': "ASZX1234!",
        }
        user = create_user(**credential)
        self.client.force_login(user)

        password_change = {
            'old_password': 'ASZX1234!',
            'new_password1': 'newASZX1234!',
            'new_password2': 'newASZX1234!', }

        res = self.client.post(PASSWORD_CHANGE_URL, follow=True, data=password_change)
        new_user = authenticate(**{
            'email': "leela@gmail.com",
            'password': "newASZX1234!",
        })

        self.assertEqual(user.pk, new_user.pk)
        self.assertEqual(res.redirect_chain[0][1], 302)
        self.assertEqual(res.status_code, 200)
