import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import Matricula

from django.contrib import messages
from django.contrib.messages import constants
import logging

def home(request):

    if  request.method == 'GET':

        return render(request, 'home.html')    
    
logger = logging.getLogger(__name__)

def nova_matricula(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_aluno = data.get('cardName')
            email_aluno  = data.get('cardEmail') or None
            fone_aluno  = data.get('cardFone')
            nasc_aluno  = data.get('cardNascimento') or None

            matricula = Matricula(
                nome_aluno=nome_aluno,      # These should match the model field names
                email_aluno=email_aluno,
                fone_aluno=fone_aluno,
                nasc_aluno=nasc_aluno,
            )
            matricula.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return JsonResponse({'message': 'Usuário cadastrado com sucesso!'}, status=200)
        except json.JSONDecodeError:
            logger.error("JSON decode error", exc_info=True)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Error in nova_matricula", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
