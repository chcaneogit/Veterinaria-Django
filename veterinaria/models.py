# models.py
from django.db import models

class Usuario(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)  
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    nacimiento = models.DateField()
    celular = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    password = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
