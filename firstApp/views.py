from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def display(request):
    return HttpResponse("<h1>Hello, World!</h1><p>This is my first Django app.</p>")

def displayDateTime(request):
    import datetime
    now = datetime.datetime.now()
    html = f"<h1>Current Date and Time</h1><p>{now}</p>"
    return HttpResponse(html)


def registro(request):
    return HttpResponse("<h1>Registro de Usuarios</h1><p>Formulario de registro (simulado).</p>")


def perfil_usuario(request, username):
    return HttpResponse(f"<h1>Perfil de {username}</h1><p>Detalles del usuario (simulado).</p>")