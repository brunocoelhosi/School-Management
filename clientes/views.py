from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

@login_required(login_url = '/auth/cadastro')
def clientes(request):
        
    if request.method == "GET":
        status = request.GET.get('status')
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes':clientes_list, 'status':status})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        datanascimento = request.POST.get('datanascimento')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        cep = request.POST.get('cep')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')
        nome_responsavel = request.POST.get('nome_responsavel')
        cpf_responsavel = request.POST.get('cpf_responsavel')
        nascimento_responsavel = request.POST.get('nascimento_responsavel')
        telefone_responsavel = request.POST.get('telefone_responsavel')
        cursos = request.POST.get('cursos')
        situacao = request.POST.get('situacao')
        duracao = request.POST.get('duracao')
        inicio = request.POST.get('inicio')
        dias_curso = request.POST.get('dias_curso')
        horarios_curso = request.POST.get('horarios_curso')
        instrutor = request.POST.get('instrutor')
        mensalidade = request.POST.get('mensalidade')
        parcelas = request.POST.get('parcelas')
        dia_pagamento = request.POST.get('dia_pagamento')
        total = request.POST.get('total_calculo')

        cliente = Cliente.objects.filter(Q(cpf=cpf)|Q(nome=nome)) #verifica se ja existe o cpf ou nome cadastrado

        if cliente.exists():
            #return HttpResponse('Cliente já cadastrado!')
            messages.add_message(request, constants.WARNING, 'Usuário já cadastrado no sistema!')
            
            return redirect('/clientes/')
  
        cliente = Cliente (
            nome = nome,
            cpf = cpf,
            datanascimento = datanascimento,
            email = email,
            endereco = endereco,
            bairro = bairro,
            cep = cep,
            cidade = cidade,
            estado = estado,
            telefone = telefone,
            celular = celular,
            nome_responsavel = nome_responsavel,
            cpf_responsavel = cpf_responsavel,
            nascimento_responsavel = nascimento_responsavel,
            telefone_responsavel = telefone_responsavel,
            cursos = cursos,
            situacao = situacao,
            duracao = duracao,
            inicio = inicio,
            dias_curso = dias_curso,
            horarios_curso = horarios_curso,
            instrutor = instrutor,
            mensalidade = mensalidade,
            parcelas = parcelas,
            dia_pagamento = dia_pagamento,
            total = total,
        )

        cliente.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        return redirect('/clientes/')



def atualiza_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=id_cliente)

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']

    data = {'cliente': cliente_json, 'cliente_id': cliente_id}
    print(data)
    return JsonResponse(data)


def update_cliente(request, id):
    body = json.loads(request.body)

    nome = body['nome']
    cpf = body['cpf']
    datanascimento = body['datanascimento']
    email = body['email']
    endereco = body['endereco']
    bairro = body['bairro']
    cep = body['cep']
    cidade = body['cidade']
    estado = body['estado']
    telefone = body['telefone']
    celular = body['celular']
    nome_responsavel = body['nome_responsavel']
    cpf_responsavel = body['cpf_responsavel']
    nascimento_responsavel = body['nascimento_responsavel']
    telefone_responsavel = body['telefone_responsavel']
    cursos = body['cursos']
    situacao = body['situacao']
    duracao = body['duracao']
    inicio = body['inicio']
    dias_curso = body['dias_curso']
    horarios_curso = body['horarios_curso']
    instrutor = body['instrutor']
    mensalidade = body['mensalidade']
    parcelas = body['parcelas']
    dia_pagamento = body['dia_pagamento']
    total = body['total']

    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.cpf = cpf
        cliente.datanascimento = datanascimento
        cliente.email = email
        cliente.endereco = endereco
        cliente.bairro = bairro
        cliente.cep = cep
        cliente.cidade = cidade
        cliente.estado = estado
        cliente.telefone = telefone
        cliente.celular = celular
        cliente.nome_responsavel = nome_responsavel
        cliente.cpf_responsavel = cpf_responsavel
        cliente.nascimento_responsavel = nascimento_responsavel
        cliente.telefone_responsavel = telefone_responsavel
        cliente.cursos = cursos
        cliente.situacao = situacao
        cliente.duracao = duracao
        cliente.inicio = inicio
        cliente.dias_curso = dias_curso
        cliente.horarios_curso = horarios_curso
        cliente.instrutor = instrutor
        cliente.mensalidade = mensalidade
        cliente.parcelas = parcelas
        cliente.dia_pagamento = dia_pagamento
        cliente.total = total
        
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'cpf':cpf, 'datanascimento':datanascimento, 'email': email, 'endereco': endereco, 'bairro': bairro, 'cep': cep,
                             'cidade': cidade, 'estado': estado, 'telefone': telefone, 'celular': celular, 'nome_responsavel': nome_responsavel, 'cpf_responsavel': cpf_responsavel,
                             'nascimento_responsavel': nascimento_responsavel, 'telefone_responsavel': telefone_responsavel, 'cursos': cursos, 'situacao': situacao, 'duracao': duracao, 'inicio': inicio,
                             'dias_curso': dias_curso, 'horarios_curso': horarios_curso, 'instrutor': instrutor, 'mensalidade': mensalidade, 'parcelas':parcelas, 'dia_pagamento':dia_pagamento, 'total': total})
    except:
        return JsonResponse({'status': '500'})
    
   
def excluir_cliente(request, id):
    if request.method == 'DELETE':
        try:
            cliente = Cliente.objects.get(id=id)
            cliente.delete()
            messages.add_message(request, constants.SUCCESS, 'cliente excluido')
            return JsonResponse({'status': '200', 'message': 'Cliente excluído com sucesso.'})
        except Cliente.DoesNotExist:
            return JsonResponse({'status': '404', 'message': 'Cliente não encontrado.'})
        
    else:
        return JsonResponse({'status': '400', 'message': 'Método não permitido.'})