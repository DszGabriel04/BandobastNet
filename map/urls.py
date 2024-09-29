from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.show_map, name='show_map'),
    path('update-json/', views.update_json_view, name='update_json'),
]
