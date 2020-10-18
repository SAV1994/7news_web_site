from django.contrib.auth.forms import AuthenticationForm


def add_login_form(request):
    if not request.user.is_authenticated:
        return {'login_form': AuthenticationForm()}
    return {'login_form': None}
