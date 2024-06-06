from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Financeiro
from .models import Cliente
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import FormFinanceiro

def financeiro(request):
    
    if request.session.get('logado'):

        if request.method == "GET":
            id_teste = request.GET.get('id_js')
            print('id python:', id_teste)

            clientes_list = Cliente.objects.all()
            
            if id_teste:
                teste_list = list(Financeiro.objects.all().values('id', 'cliente_id', 'cliente__nome','data_pagamento',
                                                                'data_vencimento','descricao_pagamento','valor_mensalidade','valor_pago').filter(cliente_id=id_teste))
            else:
                teste_list = []

            # Verificar se a solicitação é AJAX e retornar JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'testes': teste_list})

            return render(request, 'financeiro.html', {'clientes': clientes_list,'testes': teste_list})
    

        elif request.method == "POST":
            data = json.loads(request.body)
            id_java = data.get('id_java')

            # Salvar id_java na sessão (opcional, se necessário)
            request.session['id_java'] = id_java

            # Processar os dados recebidos
            result = f"ID do cliente: {id_java}"

            response = {
                'result': result
            }

            return JsonResponse(response)
    
    else:
        return redirect('/auth/login/?status=2')
    
def delete_financeiro(request, pagamento_id):
    if request.method == "DELETE":
        financeiro = get_object_or_404(Financeiro, id=pagamento_id)
        financeiro.delete()
        return JsonResponse({'message': 'Pagamento excluído com sucesso.'})
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)



def novo_pagamento(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        data_pagamento = data.get('data_pagamento')
        data_vencimento = data.get('data_vencimento')
        valor_mensalidade = data.get('valor_mensalidade')
        descricao_pagamento=data.get('descricao_pagamento')
        valor_pago = data.get('valor_pago')

        cliente = get_object_or_404(Cliente, id=cliente_id)
        financeiro = Financeiro.objects.create(cliente=cliente, data_pagamento=data_pagamento,
                                               data_vencimento = data_vencimento, valor_mensalidade = valor_mensalidade,
                                               descricao_pagamento=descricao_pagamento, valor_pago=valor_pago)
        financeiro.save()

        return JsonResponse({'message': 'Pagamento criado com sucesso.'})
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def retorna_dados10(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Financeiro.objects.filter(cliente_id=id_cliente)

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']

    data = {'cliente': cliente_json, 'cliente_id': cliente_id}
    return JsonResponse(data)



def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=id_cliente)

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']

    data = {'cliente': cliente_json, 'cliente_id': cliente_id}
  
    return JsonResponse(data)




def atualiza_financeiro(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=id_cliente)

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']

    data = {'cliente': cliente_json, 'cliente_id': cliente_id}

    return JsonResponse(data)


