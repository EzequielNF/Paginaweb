from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, PersonaForm
from django.conf import settings
from account.models import Persona
import openpyxl
import json
import os
import datetime


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
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
    return render(request, 'inicio.html')


def agregar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = PersonaForm()
    return render(request, 'agregar.html', {'form': form})


def datos_ultimo_acceso(request):
    ruta_json = os.path.join(settings.BASE_DIR, 'ultimo_acceso.json')

    if not os.path.exists(ruta_json):
        return HttpResponseNotFound('No hay datos de último acceso')

    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos_acceso = json.load(f)

    try:
        persona = Persona.objects.get(nombre=datos_acceso.get('nombre'))
        datos_acceso['apellido'] = persona.apellido
        datos_acceso['numero_casa'] = persona.numero_casa
        datos_acceso['tipo'] = persona.tipo
        datos_acceso['vehiculo'] = persona.vehiculo
        datos_acceso['patente'] = persona.patente if persona.patente else ""
    except Persona.DoesNotExist:
        pass

    return JsonResponse(datos_acceso)


# ✅ Nueva vista: Descargar registros en Excel
def descargar_excel(request):
    ruta_logs = os.path.join(settings.BASE_DIR, 'mi_app')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Registros de acceso"
    ws.append(["Nombre", "Apellido", "Número de casa", "Tipo", "Vehículo", "Patente", "Fecha y hora"])

    if os.path.exists(ruta_logs):
        for archivo in sorted(os.listdir(ruta_logs)):
            if archivo.endswith('.json'):
                with open(os.path.join(ruta_logs, archivo), 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    ws.append([
                        datos.get('nombre', ''),
                        datos.get('apellido', ''),
                        datos.get('numero_casa', ''),
                        datos.get('tipo', ''),
                        "Sí" if datos.get('vehiculo') else "No",
                        datos.get('patente', ''),
                        datos.get('fecha_hora', '')
                    ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    nombre_archivo = f'registros_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'
    wb.save(response)
    return response
