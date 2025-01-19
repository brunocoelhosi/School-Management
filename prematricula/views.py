from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers

from django.contrib.auth.decorators import login_required
import json

from home.models import Matricula

@login_required(login_url = '/auth/login')
def prematricula(request):  

    if request.method == "GET":
        matriculas = Matricula.objects.all()  # Ordena por data, mais recentes primeiro
        return render(request, 'prematricula.html', {'matriculas': matriculas})

def deletar_mensagem(request, id):
    mensagem = get_object_or_404(Matricula, id=id)  # Substitua `Mensagem` pelo modelo correspondente
    mensagem.delete()
    return redirect('prematricula')  # Substitua pelo nome da rota que lista as mensagens
