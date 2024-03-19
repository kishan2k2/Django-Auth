# I feel like there are alot of usless imports I might have to remove them.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # I believe that this line of code single handedly defies the requirement of calling the api in models, No this is required while making the migration i.e. creating the database from the model.
from .models import *


def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exist or not.

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid email')
            redirect('/register/')

        user = authenticate(username=username, password=password)

        # Authenticate the password with the username.

        if user is None:
            messages.error(request, 'Invalid-Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )


        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
         
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
     
    # Render the registration page template (GET request)
    return render(request, 'register.html')
        
        
@login_required
def show(request):
    return render(request, 'content.html')
