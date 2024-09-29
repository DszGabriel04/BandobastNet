from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, Officer, Supervisor
from excel_upload.forms import UploadFileForm  # Import your upload form
from django.http import JsonResponse
import logging
import os
import time
import json
import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)

                if role == 'officer' and hasattr(user_profile, 'officer'):
                    login(request, user)
                    request.session['username'] = username  # Store username in session
                    return redirect('officer_home')
                elif role == 'supervisor' and hasattr(user_profile, 'supervisor'):
                    login(request, user)
                    request.session['username'] = username  # Store username in session
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
            username = request.session.get('username')  # Retrieve username from session
            return render(request, 'authentication/officer_dashboard.html', {'username': username})
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
            username = request.session.get('username')  # Retrieve username from session
            return render(request, 'authentication/supervisor_dashboard.html', {'username': username})
        else:
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')


def supervisor_dashboard(request):
    form = UploadFileForm()  # Create an instance of the form
    return render(request, 'authentication/supervisor_dashboard.html', {'form': form})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only use csrf_exempt for testing; implement CSRF protection in production
@login_required  # Ensure that the user is logged in
def send_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            username = request.user.username if request.user.is_authenticated else None

            # Print latitude and longitude to the terminal
            print(f"Received Latitude: {latitude}, Longitude: {longitude} of officer {username}")

            new_data = {
                "off_name": username,
                "coords_lat": latitude,
                "coords_long": longitude,
                "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            }

            # Define the file path to save JSON data
            file_path = os.path.join('map', 'static', 'map', 'policedata.json')

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Check if the file exists
            if os.path.exists(file_path):
                # If file exists, open it in read and write mode
                with open(file_path, 'r+') as file:
                    try:
                        # Load the existing data
                        existing_data = json.load(file)
                    except json.JSONDecodeError:
                        # If the file is empty or invalid, initialize it as an empty list
                        existing_data = []

                    # Append the new data
                    existing_data.append(new_data)

                    # Move the pointer to the beginning and write the updated data
                    file.seek(0)
                    json.dump(existing_data, file, indent=4)

                    # Truncate any leftover data (in case new data is smaller)
                    file.truncate()
            else:
                # If file doesn't exist, create it and write the new data as a list
                with open(file_path, 'w') as file:
                    json.dump([new_data], file, indent=4)

            # Respond back to the client
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return JsonResponse({'status': 'fail', 'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)


def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')
