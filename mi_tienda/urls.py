"""
Configuración de URLs para el proyecto mi_tienda.
"""
from django.contrib import admin
from django.urls import path, include  # Importamos obligatoriamente 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('firstApp.urls')),   # Redirecciona a las URLs de la primera app
    path('app2/', include('secondApp.urls')),  # Redirecciona a las URLs de la segunda app
    # Rutas más amigables para el proyecto: usuarios y productos
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('secondApp.urls')),
]

