from django.urls import path
from . import views

app_name = 'excel_upload'

urlpatterns = [
    path('', views.upload, name='upload'),
]
