from django.urls import path
from . import views
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('', views.home, name = "home"),
    path('nova_matricula/', views.nova_matricula, name = "nova_matricula"),

]

    