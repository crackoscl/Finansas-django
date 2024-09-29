from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


User = get_user_model()


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email"]
        # widgets = {
        #     'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Usuario'}),
        #     'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        # }

        error_messages = {
            "username": {
                "required": "Nombre de usuario es requerido",
                "invalid": "",
            },
            "email": {
                "required": "Email es requerido",
                "invalid": "",
            }
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        existe = User.objects.filter(username__iexact=username).exists()
        if existe:
            raise forms.ValidationError("Este nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Este Email ya existe")

    # def __init__(self, *args, **kwargs):
    #     super(RegisterUserForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].widget = PasswordInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    #     self.fields['password2'].widget = PasswordInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Confirmación Contraseña'})
