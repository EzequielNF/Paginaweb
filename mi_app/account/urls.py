from .views import user_login, inicio, agregar_persona, datos_ultimo_acceso, descargar_excel
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('login/', user_login, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('agregar/', agregar_persona, name='agregar_persona'),
    path('datos-ultimo-acceso/', datos_ultimo_acceso, name='datos_ultimo_acceso'),
    path('descargar-excel/', descargar_excel, name='descargar_excel'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)