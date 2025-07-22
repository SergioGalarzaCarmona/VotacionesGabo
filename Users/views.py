from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .models import Candidates, Profile
from .forms import RegisterUser, LoginUser, VoteForm, CreateCandidateForm
from django.contrib import messages


# Create your views here.
def home(request):
    ombudmans = Candidates.objects.filter(role='Personería').order_by('-votes')
    comptrollers = Candidates.objects.filter(role='Contraloría').order_by('-votes')
    return render(request, 'users/home.html',{
        'comptrollers' : comptrollers,
        'ombudmans' : ombudmans,
    })

def logIn(request):
    logout(request)
    if request.method == 'GET':
        return render(request, 'users/logIn.html')
    else:
        #get the username by email
        try:
            user = User.objects.get(email=request.POST['email'])
        #if the email is not registered, return a error message
        except User.DoesNotExist:
            return render(request, 'Users/LogIn.html', {
                'form': LoginUser(request.POST),
                'error': 'El email no esta registrado.'
            })
        #verifies if the user is active
        if not user.is_active:
            return render(request,'users/logIn.html',{
                'form': LoginUser(request.POST),
                'error': 'Este usuario ya votó.'
            })
        if user.is_superuser:
            login(request, user)
            return redirect('admin_votes')
        #authenticate user
        user = authenticate(username=user.username, password=request.POST['password'], is_active=True)
        #If find user and two values are corrects, log in.
        if user is not None:
            login(request, user)
            return redirect('main')
        #if not find user, return a error message 
        else:
            return render(request, 'Users/logIn.html', {
                'form': LoginUser(request.POST),
                'error': 'Usuario o contraseña incorrectos'
            })

def signUp(request):
    if request.method == 'GET':
        return redirect('home')
    else:
        #create form to register user
        form = RegisterUser(request.POST)
        #if only one value of form is invalid, return the error message, and css class for fix error of margin
        if not form.is_valid():
                return render(request, 'Users/admin.html', {
                    'candidates_form' : CreateCandidateForm(),
                    'users_form' : RegisterUser(request.POST,request.FILES),
                    "checked_user" : "checked",
                })
        #if all form is valid, save it to create an user.
        user = form.save()
        #with user create a profile
        form.create_profile(user)
        return redirect('admin_votes')
    
def Logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='logIn')
def main(request):
    ombudmans = Candidates.objects.filter(role='Personería')
    comptrollers = Candidates.objects.filter(role='Contraloría')
    if request.method == 'GET':
        return render(request, 'users/main.html',{
            'form' : VoteForm(),
            'ombudmans' : ombudmans,
            'comptrollers' : comptrollers,
        })
    else:
        form = VoteForm(request.POST)
        if not form.is_valid():
            return render(request, 'users/main.html',{
                'form' : form,
                'ombudmans' : ombudmans,
                'comptrollers' : comptrollers,
                
            })
        form.save(user=request.user)
        return redirect('main')
    
@login_required(login_url='logIn')
def admin_votes(request):
    #check if the user is superuser
    if not request.user.is_superuser:
        return redirect('main')
    ombudmans = Candidates.objects.filter(role='Personería')
    comptrollers = Candidates.objects.filter(role='Contraloría')
    votes_ombudman = sum(candidate.votes for candidate in ombudmans)
    votes_comptroller = sum(candidate.votes for candidate in comptrollers)
    for candidate in ombudmans:
        candidate.percentage = (candidate.votes / votes_ombudman * 100) if votes_ombudman > 0 else 0
        candidate.save()
    for candidate in comptrollers:
        candidate.percentage = (candidate.votes / votes_comptroller * 100) if votes_comptroller > 0 else 0
        candidate.save()
    profiles = Profile.objects.all()
    candidates = Candidates.objects.all().order_by('-votes')
    votes_casted = Profile.objects.filter(voted_ombudman=True, voted_comptroller=True).count()
    users = User.objects.filter(is_superuser=False).count()
    if users > 0:
        percentage = (votes_casted / users) * 100
    else:
        percentage = 0
    if request.method == 'GET':
        return render(request,'Users/admin.html',{
            'profiles' : profiles,
            'candidates' : candidates,
            'votes_casted' : votes_casted,
            'users' : users,
            'percentage' : percentage,
        })
        
@login_required(login_url='logIn')
def create_user(request):
    if request.method != 'POST':
        return redirect('admin_votes')
    form = RegisterUser(request.POST, request.FILES)
    profiles = Profile.objects.all()
    candidates = Candidates.objects.all().order_by('-votes')
    votes_casted = Profile.objects.filter(voted_ombudman=True, voted_comptroller=True).count()
    users = User.objects.filter(is_superuser=False).count()
    if users > 0:
        percentage = (votes_casted / users) * 100
    else:
        percentage = 0
    if not form.is_valid():
        messages.warning(request, 'Hubo un error al crear el usuario. Por favor, revisa el formulario.')
        return render(request, 'Users/admin.html', {
            'users_form': RegisterUser(request.POST),
            "checked_user": "True",
            'profiles' : profiles,
            'candidates' : candidates,
            'votes_casted' : votes_casted,
            'users' : users,
            'percentage' : percentage,
        })
    user = form.save()
    form.create_profile(user)
    messages.success(request, 'Usuario creado exitosamente.')
    return redirect('admin_votes')

@login_required(login_url='logIn')
def create_candidate(request):
    if request.method != 'POST':
        return redirect('admin_votes')
    form = CreateCandidateForm(request.POST, request.FILES)
    profiles = Profile.objects.all()
    candidates = Candidates.objects.all().order_by('-votes')
    votes_casted = Profile.objects.filter(voted_ombudman=True, voted_comptroller=True).count()
    users = User.objects.filter(is_superuser=False).count()
    if users > 0:
        percentage = (votes_casted / users) * 100
    else:
        percentage = 0
    if not form.is_valid():
        messages.warning(request, 'Hubo un error al crear el candidato. Por favor, revisa el formulario.')
        return render(request, 'Users/admin.html', {
            'candidates_form': CreateCandidateForm(request.POST),
            "checked_candidate": "True",
            'profiles' : profiles,
            'candidates' : candidates,
            'votes_casted' : votes_casted,
            'users' : users,
            'percentage' : percentage,
        })
    form.save()
    messages.success(request, 'Candidato creado exitosamente.')
    return redirect('admin_votes')

@login_required(login_url='logIn')
def restart_votes(request):
    if request.method != 'POST':
        return redirect('admin_votes')
    #check if the user is superuser
    if not request.user.is_superuser:
        return redirect('main')
    call_command('flush', interactive=False)
    return redirect('home')

@login_required(login_url='logIn')
def vote(request):
    if request.method != 'POST':
        return redirect('main')
    profile = Profile.objects.get(user=request.user)
    form = VoteForm(request.POST)
    ombudmans = Candidates.objects.filter(role='Personería')
    comptrollers = Candidates.objects.filter(role='Contraloría')
    profiles = Profile.objects.all()
    candidates = Candidates.objects.all().order_by('-votes')
    votes_casted = Profile.objects.filter(voted_ombudman=True, voted_comptroller=True).count()
    users = User.objects.filter(is_superuser=False).count()
    if users > 0:
        percentage = (votes_casted / users) * 100
    else:
        percentage = 0
    if not form.is_valid():
        messages.warning(request, 'Por favor, selecciona un candidato.')
        return render(request, 'users/main.html', {
            'form': form,
            'ombudmans' : ombudmans,
            'comptrollers' : comptrollers,
            'profiles' : profiles,
            'candidates' : candidates,
            'votes_casted' : votes_casted,
            'users' : users,
            'percentage' : percentage,
        })

    candidate = form.cleaned_data.get('candidate')
    if candidate.role == 'Personería':
        if request.user.profile.voted_ombudman:
            messages.warning(request, 'Ya has votado por el personero.')
            return render(request, 'users/main.html', {
                'form': form,
                'ombudmans' : ombudmans,
                'comptrollers' : comptrollers,
                'error': 'Ya has votado por el personero.',
                'profiles' : profiles,
                'candidates' : candidates,
                'votes_casted' : votes_casted,
                'users' : users,
                'percentage' : percentage,
            })
        profile.voted_ombudman = True
        profile.save()
        candidate.votes += 1
        candidate.save()
        if request.user.profile.voted_comptroller:
            form.save(user=request.user)
    elif candidate.role == 'Contraloría':
        if request.user.profile.voted_comptroller:
            messages.warning(request, 'Ya has votado por el contralor.')
            return render(request, 'users/main.html', {
                'form': form,
                'ombudmans' : ombudmans,
                'comptrollers' : comptrollers,
                'profiles' : profiles,
                'candidates' : candidates,
                'votes_casted' : votes_casted,
                'users' : users,
                'percentage' : percentage,
            })
        profile.voted_comptroller = True
        profile.save()
        candidate.votes += 1
        candidate.save()
        if request.user.profile.voted_ombudman:
            form.save(user=request.user)
    messages.success(request, 'Voto registrado exitosamente.')
    return render(request, 'users/main.html', {
        'form': VoteForm(),
        'ombudmans' : ombudmans,
        'comptrollers' : comptrollers,
        'profiles' : profiles,
        'candidates' : candidates,
        'votes_casted' : votes_casted,
        'users' : users,
        'percentage' : percentage,
    }
    )