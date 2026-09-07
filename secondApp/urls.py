from django.urls import path
from .views import saludo_app2, PaginaApp2

urlpatterns = [
    path('inicio/', saludo_app2, name='saludo_app2'),
    path('perfil/', PaginaApp2.as_view(), name='perfil_app2'),
]
