from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render
from .forms import TaskForm
from .models import Task

def home(request):
    return render(request, "home.html")

def taskss(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "taskss.html",
                  {'tasks': tasks})
 
def create_task(request):
    if request.method == 'GET':
        return render(request, 
                   "create_task.html",
                   {"forms":TaskForm})
    else: 
        try:
            forms = TaskForm(request.POST)
            new_task = forms.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('taskss')
        except ValueError:
           return render(request,
                      'create_task.html',
                      {'forms': TaskForm,
                       'error': "por favor ingresa datos validos"})

def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, 
                  "signin.html",
                  {"form":AuthenticationForm})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,
                          'signin.html',
                          {"form": AuthenticationForm(),
                           "error":"Usuario o contraseña incorrecta"})
        else:
            login(request, user)
            return redirect("taskss")

def singup(request):
    if request.method == "GET":
        return render(request, 
                  "singup.html",
                  {"form":UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("taskss")

            except IntegrityError:
                return render(request,
                              'singup.html',
                              {"form": UserCreationForm(),
                               "error":"Error al crear el usuario"})

        else:
                 return render(request,
                              'singup.html',
                              {"form": UserCreationForm(),
                               "error":"Error, Las contraseñas no coinciden"})
