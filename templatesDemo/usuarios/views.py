from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404


def logout_usuario(request):
    logout(request)
    return redirect('/')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guardar email y nombre adicional si vienen en el POST
            user = form.save(commit=False)
            email = request.POST.get('email', '').strip()
            name = request.POST.get('name', '').strip()
            if email:
                user.email = email
            if name:
                user.first_name = name
            user.save()
            login(request, user)
            return redirect('usuarios:perfil_usuario', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})


@login_required
def perfil_usuario(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'usuarios/profile.html', {'profile_user': user})
