from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'website/layout.html')

def login(request):
    return render(request, 'website/login.html')

def register(request):
    return render(request, 'website/register.html')

def cart(request):
    return

def menu(request):
    return