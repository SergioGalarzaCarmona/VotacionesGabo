from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser, LoginUser, VoteForm

# Create your views here.
def home(request):
    return render(request, 'users/home.html')

def logIn(request):
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
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'users/signUp.html')
    else:
        #create form to register user
        form = RegisterUser(request.POST)
        #if only one value of form is invalid, return the error message, and css class for fix error of margin
        if not form.is_valid():
                return render(request, 'Users/signUp.html', {
                    'form': RegisterUser(request.POST,request.FILES),
                })
        #if all form is valid, save it to create an user.
        user = form.save()
        #with user create a profile
        form.create_profile(user)
        #login the user
        login(request, user)
        return redirect('main')
    
def Logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='logIn')
def main(request):
    if request.method == 'GET':
        return render(request, 'users/main.html',{
            'form' : VoteForm(),
        })
    else:
        form = VoteForm(request.POST)
        if not form.is_valid():
            return render(request, 'users/main.html',{
                'form' : form
            })
        form.save(user=request.user)
        return redirect('main')
    
@login_required(login_url='logIn')
def admin_votes(request):

    if request.method == 'GET':
        return render(request,'Users/admin.html')