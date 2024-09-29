from django.contrib import admin
from django.urls import path, include
import map
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supervisor_home/upload/', include('excel_upload.urls')),
    path('supervisor_home/map/', include('map.urls')),
    path('', views.redirect_to_login, name='redirect_to_login'),
    path('email_notifier/', include('email_notifier.urls')),
    path('', include('pwa.urls')),
    path('', include('authentication.urls')),
]
