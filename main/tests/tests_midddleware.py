from django.test import TestCase

from ..models import User


class TestAddLoginForm(TestCase):
    def test_get_login_form_for_not_authenticated_user(self):
        resp = self.client.get('/')
        self.assertIsNotNone(resp.context['login_form'])

    def test_not_get_login_form_for_authenticated_user(self):
        user = User.objects.create(email='test@test.com', first_name='Ivan', last_name='Ivanov')
        user.set_password('123qwe321')
        user.save()
        self.client.login(email='test@test.com', password='123qwe321')
        resp = self.client.get('/')
        self.assertIsNone(resp.context['login_form'])
