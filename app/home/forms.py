from django_registration.forms import RegistrationForm
from django.contrib.auth import get_user_model


class CustomUserForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'class': 'form-control'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control'})

    class Meta(RegistrationForm.Meta):
        model = get_user_model()
