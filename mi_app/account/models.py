from django.db import models
from django.utils import timezone

class Persona(models.Model):
    TIPO_CHOICES = [
        ('residente', 'Residente'),
        ('visitante', 'Visitante'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)  # Aquí agregamos choices
    vehiculo = models.BooleanField(default=False)
    patente = models.CharField(max_length=10, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_personas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_casa}"

class RegistroAcceso(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    imagen_acceso = models.ImageField(upload_to='logs/', blank=True, null=True)

    def __str__(self):
        return f"{self.persona.nombre} {self.persona.apellido} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
# Create your models here.
