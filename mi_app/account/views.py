from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import PersonaForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('inicio')
                else:
                    return HttpResponse('Cuenta inactiva')
            else:
                return HttpResponse('Nombre de usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})            
            
def inicio(request): 
    persona = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'numero_casa': 'A12',
        'tipo': 'Residente',
        'vehiculo': True,
        'patente': 'XY-1234',
    }
    return render(request, 'inicio.html', {'persona': persona})

def agregar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = PersonaForm()
    return render(request, 'agregar.html', {'form': form})

