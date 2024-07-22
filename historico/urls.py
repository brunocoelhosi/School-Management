from django.urls import path
from . import views
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('', views.historico, name = "historico"),
    path('contrato_generator/<int:clienteId>/', views.contrato_generator, name = "contrato_generator"),
    path('ficha_generator/<int:clienteId>/', views.ficha_generator, name = "ficha_generator"),


]

