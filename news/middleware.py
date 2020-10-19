from main.forms import UserAuthenticationForm


def add_login_form(request):
    if not request.user.is_authenticated:
        return {'login_form': UserAuthenticationForm()}
    return {'login_form': None}
