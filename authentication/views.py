from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # Role selected by user

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role == role:
                login(request, user)

                # Redirect based on role
                if role == 'officer':
                    return redirect('officer_home')  # Redirect to officer home page
                elif role == 'supervisor':
                    return redirect('supervisor_home')  # Redirect to supervisor home page
            else:
                return render(request, 'authentication/login.html', {'error': 'Incorrect role selected.'})
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'authentication/login.html')


def officer_home(request):
    return render(request, 'authentication/officer_home.html')  # Create this template

def supervisor_home(request):
    return render(request, 'authentication/supervisor_home.html')  # Create this template
