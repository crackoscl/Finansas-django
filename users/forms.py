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
            },
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "phone",
            "city",
            "country",
            "about_me",
        ]
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Usuario'}),
             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
             'first_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
             'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
             'profile_image': forms.FileInput(
            attrs ={'class': 'form-control'}),
             'phone':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
             'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Ciudad'}),
             'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais'}),
             'about_me': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Acerca de mi'}),

         }
