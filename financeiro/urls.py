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

    path('', views.financeiro, name = "financeiro"),
    path('delete/<int:pagamento_id>/', views.delete_financeiro, name='delete_financeiro'),
    path('novo_pagamento/', views.novo_pagamento, name = "novo_pagamento"),
    path('comprovante_generator/<int:pagamento_id>/', views.comprovante_generator, name = "comprovante_generator"),


]

