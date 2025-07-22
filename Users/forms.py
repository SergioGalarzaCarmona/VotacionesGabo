from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Candidates
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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
    grade = forms.ChoiceField(
        choices=[(f'{i}-{j}',f'{i}-{j}') for i in range(1,12) for j in range(1,7)],
        label='Grado',
        required=True,
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
        fields = ['username', 'email','grade','identity','password1', 'password2']
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
    def clean_identity(self):
        identity = self.cleaned_data['identity']
        if Profile.objects.filter(identification=identity).exists():
            raise forms.ValidationError('La identificación ya está registrada.')
        if len(str(identity)) < 6:
            raise forms.ValidationError('La identificación debe tener al menos 6 dígitos.')
        return identity
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
        
class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=Candidates.objects.all(),
        label='Candidato',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
        
    def save(self,user = None):
        candidate = self.cleaned_data.get('candidate')
        if candidate:
            candidate.votes += 1
            candidate.save()
        if user:
            user.is_active = False
            user.save()
        
        
class CreateCandidateForm(forms.ModelForm):
    
    profile = forms.ModelChoiceField(
        queryset=Profile.objects.filter(grade__startswith='11-'),
        label='Estudiante',
        required=True,
    )
    description = forms.CharField(
        max_length=500,
        label='Descripción',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Descripción',
            }
        )
    )
    image = forms.ImageField(
        label='Imagen',
        required=False
    )
    class Meta:
        model = Candidates
        fields = ['profile', 'description', 'image']
        
    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if Candidates.objects.filter(profile=profile).exists():
            raise ValidationError(f'El candidato ya esta registrado.')
        return profile
    
