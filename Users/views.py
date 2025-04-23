from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser, LoginUser

# Create your views here.
def home(request):
    return render(request, 'users/home.html')

#Function used in other view
def logIn(request):
    if request.method == 'GET':
        return render(request, 'users/logIn.html')
    else:
        #authenticate user
        user = authenticate(username=request.POST['username'], password=request.POST['password'], is_active=True)
        #If find user and two values are corrects, log in.
        if user is not None:
            login(request, user)
            return redirect('main')
        #if not find user, return a error message 
        else:
            return render(request, 'Users/authenticate.html', {
                'form': LoginUser(request.POST),
                'error': 'Usuario o contraseña incorrectos'
            })

def signUp(request):
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
        #If the user uploads an image, the image will have that value, otherwise, it will have a default value.
        image = request.FILES.get('image','default.jpg')
        #with user and image create a profile
        form.create_profile(user,image)
        #login the user
        login(request, user)
        return redirect('main')
    
def Logout(request):
    logout(request)
    return redirect('home')