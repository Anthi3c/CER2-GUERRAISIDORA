from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, Inscrito
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Count


# Create your views here.

def e_destacado(request):
    return render(request, 'core/e_destacado.html', {})


def lista_e(request):
    """eventos=Evento.objects.all()
    inscritos = Inscrito.objects.all()
    return render(request, 'core/lista_e.html', {'eventos': eventos, 'inscritos':inscritos})"""

    eventos = Evento.objects.annotate(inscritos_count=Count('evento_inscrito'))
    if request.user.is_authenticated:
        inscritos_event_ids = set(
            Inscrito.objects.filter(usuario=request.user).values_list('evento_id', flat=True)
        )
    else:
        inscritos_event_ids = set()

    if request.method == 'POST' and request.user.is_authenticated:
        action = request.POST.get('action')
        event_id = request.POST.get('event_id')
        if not event_id:
            messages.error(request, "Evento no especificado.")
            return redirect('lista_e')

        db_engine = request.session.get('_db_engine') #manejo base de datos
        try:
            #uso de MySQL o PostgreSQL
            with transaction.atomic():
                evento = Evento.objects.select_for_update().get(pk=event_id)
                inscritos_count = Inscrito.objects.filter(evento=evento).count()
                disponibles = max(0, evento.cupos - inscritos_count)

                if action == 'inscribir':
                    if disponibles <= 0:
                        messages.error(request, f"No hay cupos disponibles en {evento.nombre}.")
                    else:
                        obj, created = Inscrito.objects.get_or_create(usuario=request.user, evento=evento)
                        if created:
                            messages.success(request, f"Te inscribiste en {evento.nombre}.")
                        else:
                            messages.info(request, f"Ya estabas inscrito en {evento.nombre}.")
                elif action == 'desinscribir':
                    deleted = Inscrito.objects.filter(usuario=request.user, evento=evento).delete()
                    messages.success(request, f"Te desinscribiste de {evento.nombre}.")
                else:
                    messages.error(request, "Acción desconocida.")
        except Evento.DoesNotExist:
            messages.error(request, "Evento no existe.")
        except IntegrityError:
            messages.error(request, "Error al procesar la inscripción (intenta de nuevo).")

        return redirect('lista_e')
    
    for e in eventos:
        e.cupos_disponibles = max(0, e.cupos - getattr(e, 'inscritos_count', 0))

    return render(request, 'core/lista_e.html', {
        'eventos': eventos,
        'inscritos_event_ids': inscritos_event_ids,
    })

def comunidad(request):
    return render(request, 'core/comunidad.html', {})
