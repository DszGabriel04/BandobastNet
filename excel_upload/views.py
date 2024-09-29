import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from authentication.models import Officer  # Import the Officer model
from django.utils import timezone

def upload(request):
    data = None
    redirect_url = request.GET.get('redirect', 'excel_upload:upload')  # Default to 'upload' if no redirect provided

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            # Read the excel file using pandas
            df = pd.read_excel(excel_file)

            # Create a set of usernames from the Excel sheet
            excel_usernames = set(df['username'].values)

            # Convert the datetime columns
            df['duty_time_start'] = pd.to_datetime(df['duty_time_start'], errors='coerce')
            df['duty_time_end'] = pd.to_datetime(df['duty_time_end'], errors='coerce')

            # Iterate through the rows in the DataFrame
            for index, row in df.iterrows():
                username = row['username']
                duty_coord_lat = row.get('duty_coord_lat')
                duty_coord_long = row.get('duty_coord_long')
                radius_of_duty = row.get('radius_of_duty')
                duty_time_start = row.get('duty_time_start')
                duty_time_end = row.get('duty_time_end')

                try:
                    # Try to fetch the officer by username
                    officer = Officer.objects.get(user_profile__user__username=username)
                    # If found, update the officer's attributes and set is_on_duty to True
                    officer.duty_coord_lat = duty_coord_lat
                    officer.duty_coord_long = duty_coord_long
                    officer.radius_of_duty = radius_of_duty
                    officer.is_on_duty = True
                    officer.duty_time_start = duty_time_start if pd.notnull(duty_time_start) else timezone.now()
                    officer.duty_time_end = duty_time_end if pd.notnull(duty_time_end) else None
                    officer.save()
                except Officer.DoesNotExist:
                    # If not found, just skip (since it should already exist in the database)
                    continue

            # Now set attributes for all officers not in the Excel sheet to null and is_on_duty to False
            Officer.objects.exclude(user_profile__user__username__in=excel_usernames).update(
                duty_coord_lat=None,
                duty_coord_long=None,
                radius_of_duty=None,
                duty_time_start=None,
                duty_time_end=None,
                is_on_duty=False
            )

            # Redirect after processing
            return redirect(redirect_url)  # Redirect to the page passed in the query parameter

    else:
        form = UploadFileForm()

    return render(request, 'authentication/supervisor_dashboard.html', {'form': form, 'data': data})
