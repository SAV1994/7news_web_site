from django.test import TestCase

from ..forms import UserForm, UserAuthenticationForm


class UserFormTest(TestCase):
    def test_password_label(self):
        form = UserForm()
        self.assertEqual(form.fields['password'].label, 'Password')

    def test_password_min_length(self):
        form = UserForm()
        self.assertEqual(form.fields['password'].min_length, 6)

    def test_password_confirmation_label(self):
        form = UserForm()
        self.assertEqual(form.fields['password_confirmation'].label, 'Confirm password')

    def test_consent_with_rules_label(self):
        form = UserForm()
        self.assertEqual(form.fields['consent_with_rules'].label, 'I agree 7NEWS rules')

    def test_registration_with_incorrect_confirm_password(self):
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'ivanov@ivan.com', 'password': '123qwe321',
                'password_confirmation': '123qwe320', 'consent_with_rules': 'True'}
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_registration_success(self):
        data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'ivanov@ivan.com', 'password': '123qwe321',
                'password_confirmation': '123qwe321', 'consent_with_rules': True}
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())


class UserAuthenticationFormTest(TestCase):
    def test_password_label(self):
        form = UserAuthenticationForm()
        self.assertEqual(form.fields['password'].label, 'Password')

    def test_password_min_length(self):
        form = UserAuthenticationForm()
        self.assertEqual(form.fields['password'].min_length, 6)
