from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms  import UserCreationForm
# Create your views here.
def singup(request):
    return render(request, 
                  "singup.html",
                  {"form": UserCreationForm})