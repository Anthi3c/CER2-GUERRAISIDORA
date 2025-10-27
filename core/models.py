from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    valor = models.IntegerField()
    cupos = models.IntegerField()

    def __str__(self):
        return self.nombre
    
    @property
    def inscritos_count(self):
        if hasattr(self, '_inscritos_count'):
            return int(self._inscritos_count) or 0
        return self.evento_inscrito.count()

    @property
    def cupos_disponibles(self):
        return max(0, int(self.cupos or 0) - self.inscritos_count)

    def clean(self):
        # evitar que se reduzcan cupos por debajo de inscritos actuales
        if self.pk:
            current_inscritos = self.evento_inscrito.count()
            if self.cupos < current_inscritos:
                raise ValidationError({
                    'cupos': f"No puedes fijar cupos a {self.cupos}: ya hay {current_inscritos} inscritos."
                })


class Inscrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_inscrito")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="evento_inscrito")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='unique_inscripcion')
        ]

    def __str__(self):
        return f"{self.usuario.username} -> {self.evento.nombre}"


    def clean(self):
        # comprobar cupos antes de guardar (excluye este objeto si ya existe)
        if not self.evento:
            return
        qs = Inscrito.objects.filter(evento=self.evento)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        inscritos_count = qs.count()
        if inscritos_count >= self.evento.cupos:
            raise ValidationError("No hay cupos disponibles para este evento.")

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                Evento.objects.select_for_update().get(pk=self.evento_id)
                self.full_clean()
                super().save(*args, **kwargs)
        else:
            self.full_clean()
            super().save(*args, **kwargs)