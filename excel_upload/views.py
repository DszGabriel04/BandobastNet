import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm

def upload(request):
    data = None
    redirect_url = request.GET.get('redirect', 'default_view')  # Set a default if needed

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            # Read the excel file using pandas
            df = pd.read_excel(excel_file)

            data = df.to_html()

            # After processing, redirect to the specified URL
            return redirect(redirect_url)  # Redirect to the page passed in the query parameter

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'data': data})
