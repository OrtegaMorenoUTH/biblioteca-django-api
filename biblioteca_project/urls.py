# biblioteca_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # ✨ URLs de la API (AGREGAR ESTA LÍNEA)
    path('api/', include('libros.api_urls')),
]