from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, PermissionsGroup
from django.core.exceptions import ValidationError


class RegisterUser(UserCreationForm):
    
    image = forms.ImageField(
        label='Imagen de Perfil', 
        required=False, 
        widget=forms.FileInput(
            attrs={
                'class' : ''
                }
            )
        )
    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario',
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de Usuario',
                'class' : ''
                }
            )
        )
    email = forms.EmailField(
        max_length=254,
        label='Correo Electrónico',
        required=True, 
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class' : ''
                }
            )
        )
    password1 = forms.CharField(
        max_length=30,
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    password2 = forms.CharField(
        max_length=30,
        label='Confirmacion de Contraseña',
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar Contraseña',
                'class' : ''
                }
            )
        )
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        if len(username) < 8:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 8 caracteres.')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado.')
        return email
    
    def create_profile(self,user,image = None):
        if image == None:
            image = 'default.jpg'
        Profile.objects.create(user=user,image=image)

#Form to login
class LoginUser(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        label='Nombre de Usuario', 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de Usuario',
                'class' : ''
                }
            )
        )
    password = forms.CharField(
        max_length=30,
        label='Contraseña', 
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class' : ''
                }
            )
        )
    
    class Meta:
        model = User
        fields = ['username', 'password']