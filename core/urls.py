from django.urls import path
from . import views

urlpatterns = [
    path('', views.e_destacado, name='e_destacado'),
    path('lista_e', views.lista_e, name='lista_e'),
    path('comunidad', views.comunidad, name='comunidad'),
]

