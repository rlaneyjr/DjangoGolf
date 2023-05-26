from django_registration.forms import RegistrationForm
from django.contrib.auth import get_user_model


class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = get_user_model()
