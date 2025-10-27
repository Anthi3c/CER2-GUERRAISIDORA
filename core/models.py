# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    valor = models.IntegerField()
    cupos = models.IntegerField()

    def __str__(self):
        return self.nombre

class Inscrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_inscrito")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="evento_inscrito")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='unique_inscripcion')
        ]

    def __str__(self):
        return f"{self.usuario.username} -> {self.evento.nombre}"
