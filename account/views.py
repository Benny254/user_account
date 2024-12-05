from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Item

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid KeyError
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required')
            return render(request, 'account/register.html')  # Render the form again with errors

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')  # Redirect to login page on success

    # Render the registration form for GET requests or invalid submissions
    return render(request, 'account/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect("login")

def home(request):
    Items = Item.objects.all()
    return render(request, 'account/home.html',{"items": Items})            