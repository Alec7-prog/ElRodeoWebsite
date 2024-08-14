from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import User

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "website/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "website/login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)


        if user.exists():
            messages.info(request, "User already exists")
            return redirect('register')

        user = User.objects.create_user(email, password, first_name, last_name)
        

        messages.info(request, "Account Created Successfully!")
        return redirect('menu')
    
    return render(request, "website/register.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def cart(request):
    return

def menu(request):
    return render(request, "website/menu.html")