from django.urls import path
from . import views
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    #path('cadastro/', views.cadastro, name = "cadastro"),
    path('login/', views.login, name="login"),
    path('valida_cadastro/', views.valida_cadastro, name="valida_cadastro"),
    path('valida_login/', views.valida_login, name="valida_login"),
    path('sair/', views.sair, name="sair"),

]

