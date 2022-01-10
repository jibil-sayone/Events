from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = auth.authenticate(username=username, password=password)
        if users is not None:
            auth.login(request, users)
            return redirect('index')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('index')