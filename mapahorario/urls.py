from django.urls import path
from . import views


urlpatterns = [

    path('', views.mapahorario, name ="mapahorario"),

]

