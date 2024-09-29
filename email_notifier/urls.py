# email_notifier/urls.py

from django.urls import path
from .views import schedule_email

app_name = 'email_notifier'

urlpatterns = [
    path('send_email/', schedule_email, name='schedule_email'),
]
