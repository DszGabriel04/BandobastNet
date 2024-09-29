from django.contrib import admin
from django.urls import path, include
import map

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supervisor_home/upload/', include('excel_upload.urls')),
    path('supervisor_home/map/', include('map.urls')),
    path('', include('authentication.urls')),
]
