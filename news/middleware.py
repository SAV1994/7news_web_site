from main.forms import UserAuthenticationForm


def add_login_form(request):
    """Add UserAuthenticationForm to context for modal login window"""

    if not request.user.is_authenticated:
        return {'login_form': UserAuthenticationForm()}
    return {'login_form': None}
