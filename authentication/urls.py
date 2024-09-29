from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/officer/', views.officer_home, name='officer_home'),
    path('home/supervisor/', views.supervisor_home, name='supervisor_home'),
    path('track-location/', views.send_location, name='track_location'),  # New endpoint
]
