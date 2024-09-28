import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from authentication.models import Officer  # Import the Officer model

def upload(request):
    data = None
    redirect_url = request.GET.get('redirect', 'default_view')  # Set a default if needed

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            # Read the excel file using pandas
            df = pd.read_excel(excel_file)

            # Extract usernames from the DataFrame
            uploaded_usernames = df['username'].tolist()  # Assuming the column is named 'username'

            # Get all officers
            officers = Officer.objects.select_related('user_profile__user').all()

            # Create a set for fast lookup of uploaded usernames
            uploaded_usernames_set = set(uploaded_usernames)

            # Update is_on_duty for each officer
            for officer in officers:
                if officer.user_profile.user.username in uploaded_usernames_set:
                    officer.is_on_duty = True  # Set to True if found in the uploaded list
                else:
                    officer.is_on_duty = False  # Set to False if not found
                officer.save()  # Save the changes

            # Optionally display the uploaded data
            data = df.to_html()  

            # After processing, redirect to the specified URL
            #return redirect(redirect_url)  # Redirect to the page passed in the query parameter
            return redirect('excel_upload:upload')

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'data': data})
