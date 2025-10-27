from django.urls import path
from . import views

urlpatterns=[
    path('loguearse', views.loguearse, name='login'),
    path('salir', views.salir, name='logout'),
    path('registrar', views.registrar, name='registrar')
]