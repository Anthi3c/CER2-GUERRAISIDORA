from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    nombre = models.CharField()
    fecha = models.DateTimeField()
    lugar = models.CharField()
    valor = models.IntegerField()
    cupos= models.IntegerField()
  

    def __str__(self):
        return self.nombre
    
class Inscrito(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    inscripcion= models.ManyToManyField(Evento, blank=True)  

    def __str__(self):
        return self.inscripcion

