from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role == role:
                login(request, user)

                # Redirect based on role
                if role == 'officer':
                    return redirect('officer_home')
                elif role == 'supervisor':
                    # return redirect(reverse('excel_upload:upload'))
                    return redirect('supervisor_home')
            else:
                return render(request, 'authentication/login.html', {'error': 'Incorrect role selected.'})
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'authentication/login.html')


@login_required
def officer_home(request):
    return render(request, 'authentication/officer_home.html')

@login_required
def supervisor_home(request):
    return render(request, 'authentication/supervisor_home.html')
