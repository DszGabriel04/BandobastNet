import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    data = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            # Read the excel file using pandas
            df = pd.read_excel(excel_file)
            # Convert dataframe to HTML for easy rendering
            data = df.to_html()
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'data': data})
