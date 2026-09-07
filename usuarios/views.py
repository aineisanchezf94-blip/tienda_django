from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('usuarios:perfil_usuario', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})


@login_required
def perfil_usuario(request, username):
    # Permite ver el perfil propio o de otros (si se desea)
    user = get_object_or_404(User, username=username)
    return render(request, 'usuarios/profile.html', {'profile_user': user})
