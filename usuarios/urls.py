from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
]
