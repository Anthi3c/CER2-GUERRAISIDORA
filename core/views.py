from django.shortcuts import render
from .models import Evento, Inscrito

# Create your views here.

def e_destacado(request):
    return render(request, 'core/e_destacado.html', {})


def lista_e(request):
    eventos=Evento.objects.all()
    inscritos = Inscrito.objects.all()
    return render(request, 'core/lista_e.html', {'eventos': eventos, 'inscritos':inscritos})

def comunidad(request):
    return render(request, 'core/comunidad.html', {})
