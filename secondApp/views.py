from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def saludo_app2(request):
    return HttpResponse("<h1>Hola desde la segunda aplicación!</h1><p>Esta es mi segunda aplicación Django.</p>")

class PaginaApp2(View):
    def get(self, request):
        return HttpResponse("<h1>Página de la segunda aplicación</h1><p>Bienvenido a la segunda aplicación Django.</p>")
