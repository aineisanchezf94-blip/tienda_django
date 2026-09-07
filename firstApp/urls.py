from django.urls import path
from . import views

urlpatterns = [
    path('hola/', views.display, name='display'),
    path('ahora/', views.displayDateTime, name='display_datetime'),
    path('registro/', views.registro, name='registro'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
]
