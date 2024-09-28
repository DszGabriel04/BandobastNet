from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, Officer, Supervisor
from excel_upload.forms import UploadFileForm  # Import your upload form
from django.http import JsonResponse
import logging
import json

def login_view(request):
    if request.method == 'POST':
        # options presented on the form
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)

                # Check if the user is an officer or supervisor
                if role == 'officer' and hasattr(user_profile, 'officer'):
                    login(request, user)
                    # resolve the url path defined in urls.py, which then calls officer_home
                    return redirect('officer_home')
                elif role == 'supervisor' and hasattr(user_profile, 'supervisor'):
                    login(request, user)
                    return redirect('supervisor_home')
                else:
                    return render(request, 'authentication/login.html', {'error': 'Incorrect role selected.'})

            except UserProfile.DoesNotExist:
                return render(request, 'authentication/login.html', {'error': 'User profile not found.'})

        return render(request, 'authentication/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'authentication/login.html')


@login_required
def officer_home(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        # Check if the user is an officer
        if hasattr(user_profile, 'officer'):
            return render(request, 'authentication/officer_dashboard.html')                     #
        else:
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')


@login_required
def supervisor_home(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        # Check if the user is a supervisor
        if hasattr(user_profile, 'supervisor'):
            return render(request, 'authentication/supervisor_dashboard.html')                    #return render(request, 'authentication/supervisor_home.html')                                       #HERE
        else:
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')


def supervisor_dashboard(request):
    form = UploadFileForm()  # Create an instance of the form
    return render(request, 'authentication/supervisor_dashboard.html', {'form': form})

# authentication/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Only use csrf_exempt for testing; implement CSRF protection in production
def send_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # Print latitude and longitude to the terminal
            print(f"Received Latitude: {latitude}, Longitude: {longitude}")

            # Respond back to the client
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return JsonResponse({'status': 'fail', 'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)
