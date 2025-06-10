from .views import user_login, inicio, agregar_persona
from django.urls import path



urlpatterns = [

    path('login/', user_login, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('agregar/', agregar_persona, name='agregar_persona'),


]