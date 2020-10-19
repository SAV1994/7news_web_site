from django import forms
from .models import User, News, Comment
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=128, min_length=6, widget=forms.PasswordInput,
                               help_text=password_validation.password_validators_help_text_html)
    password_confirmation = forms.CharField(label='Confirm password', max_length=128, widget=forms.PasswordInput)
    consent_with_rules = forms.BooleanField(label='I agree 7NEWS rules')

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password_validation.validate_password(password)
        password_confirmation = self.cleaned_data['password_confirmation']
        consent_with_rules = self.cleaned_data['consent_with_rules']
        if password and password_confirmation and password != password_confirmation:
            errors = {'password_confirmation': ValidationError('Password mismatch', code='password_mismatch')}
            raise ValidationError(errors)
        if not consent_with_rules:
            errors = {'consent_with_rules': ValidationError('You must accept 7news rules to use our service',
                                                            code='invalid_value')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'consent_with_rules', 'password', 'password_confirmation']


class UserUpdateForm(UserForm):
    consent_with_rules = forms.BooleanField(label='I agree 7NEWS rules', widget=forms.HiddenInput, initial=True)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'news': forms.HiddenInput, 'comment': forms.HiddenInput, 'author': forms.HiddenInput}


class UserAuthenticationForm(AuthenticationForm):
    password = forms.CharField(label='Password', strip=False, min_length=6,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
