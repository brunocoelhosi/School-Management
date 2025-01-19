from django.urls import path
from . import views

urlpatterns = [
    path('', views.prematricula, name = "prematricula"),
    path('mensagens/deletar/<int:id>/', views.deletar_mensagem, name='deletar_mensagem')
]