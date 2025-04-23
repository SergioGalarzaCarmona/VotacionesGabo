from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.core.exceptions import ValidationError


class RegisterUser(UserCreationForm):
    
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
    grade = forms.CharField(
        max_length=10,
        label='Grado',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Grado',
                'class' : ''
                }
            )
        )
    identity = forms.IntegerField(    
        label='Identificación',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Identificación',
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
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    def create_profile(self,user):
        grade = self.cleaned_data.get('grade')
        identity = self.cleaned_data.get('identity')
        return Profile.objects.create(user=user, grade=grade, identification=identity)
        

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