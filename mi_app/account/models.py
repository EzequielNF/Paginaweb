from django.db import models

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

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_casa}"

# Create your models here.
