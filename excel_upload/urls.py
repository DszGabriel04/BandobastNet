from django.urls import path
from .views import upload_file

app_name = 'excel_upload'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
]
