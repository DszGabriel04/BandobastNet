from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supervisor_home/upload/', include('excel_upload.urls')), # Include the urls from an app
    path('', include('authentication.urls')),
]
