from django.contrib import admin
from django.db import transaction
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Evento, Inscrito

class InscritoAdminForm(ModelForm):
    class Meta:
        model = Inscrito
        fields = '__all__'

class InscritoAdmin(admin.ModelAdmin):
    form = InscritoAdminForm
    list_display = ('usuario', 'evento')
    search_fields = ('usuario__username', 'evento__nombre')

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                if obj.evento_id:
                    Evento.objects.select_for_update().get(pk=obj.evento_id)

                qs = Inscrito.objects.filter(evento=obj.evento)
                if change and obj.pk:
                    qs = qs.exclude(pk=obj.pk)
                inscritos_count = qs.count()

                if inscritos_count >= obj.evento.cupos:
                    form.add_error(None, ValidationError("No hay cupos disponibles para este evento."))
                    return

                obj.full_clean()
                super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)
            return
        except Evento.DoesNotExist:
            form.add_error('evento', ValidationError("El evento seleccionado no existe."))
            return

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'fecha', 'cupos', 'inscritos_count_display',
        'cupos_disponibles_display', 'recaudado_display'
    )
    readonly_fields = ('inscritos_count_display', 'cupos_disponibles_display', 'recaudado_display')
    search_fields = ('nombre', 'lugar')
    ordering = ('-fecha',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_inscritos_count=Count('evento_inscrito'))

    def inscritos_count_display(self, obj):
        return getattr(obj, '_inscritos_count', obj.evento_inscrito.count())
    inscritos_count_display.short_description = 'Inscritos'

    def cupos_disponibles_display(self, obj):
        inscritos = getattr(obj, '_inscritos_count', None)
        if inscritos is None:
            inscritos = obj.evento_inscrito.count()
        return max(0, obj.cupos - inscritos)
    cupos_disponibles_display.short_description = 'Cupos disponibles'

    def recaudado_display(self, obj):
        inscritos = getattr(obj, '_inscritos_count', None)
        if inscritos is None:
            inscritos = obj.evento_inscrito.count()
        total = (obj.valor or 0) * inscritos
        return f"${total:,}"
    recaudado_display.short_description = 'Recaudado'

admin.site.register(Inscrito, InscritoAdmin)
