from django.urls import path
from . import views
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.clientes, name ="clientes"),
    path('atualiza_cliente/', views.atualiza_cliente, name = "atualiza_cliente"),
    path('update_cliente/<int:id>', views.update_cliente, name="update_cliente"),
    path('excluir_cliente/<int:id>/', views.excluir_cliente, name="excluir_cliente")

]


