from django.shortcuts import render
# login and register form 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from . form import ContactForm
from .models import *

# Create your views here.

def index(request):
    data={
        'products':Product.objects.all()
    }
    return render(request, 'pages/index.html', data)


def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            return render(request, 'pages/login.html')
    else:
        data={
            'form': AuthenticationForm()
        }
        return render(request, 'pages/login.html', data)

def user_logout(request):
    logout(request)
    return render(request, 'pages/index.html')


def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            data={
                'form': form
            }
            return render(request, 'pages/register.html', data)
    else:
        data={
            'form': UserCreationForm()
        }
        return render(request, 'pages/register.html', data)
    


def contact(request):
        if request.method=="POST":
            form=ContactForm(request.POST)
            if form.is_valid():
                # form.save()
                return render(request, 'pages/index.html')
            else:
                data={
                    'form': form
                }
                return render(request, 'pages/contact.html', data)
        else:
            data={
                'form': ContactForm()
            }
            return render(request, 'pages/contact.html', data)  