from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from django.contrib.auth.decorators import login_required
import json

from .models import Financeiro
from .models import Cliente

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


@login_required(login_url = '/auth/login')
def financeiro(request):  

    if request.method == "GET":
        id_teste = request.GET.get('id_js')
        print('id python:', id_teste)

        clientes_list = Cliente.objects.all()
        
        if id_teste:
            financeiro_list = list(Financeiro.objects.all().values('id',
                                                                    'cliente_id',
                                                                    'cliente__nome',
                                                                    'data_pagamento',
                                                                    'data_vencimento',
                                                                    'descricao_pagamento',
                                                                    'valor_mensalidade',
                                                                    'valor_com_juros',
                                                                    'valor_pago').filter(cliente_id=id_teste))
            
            for financeiro in financeiro_list:
                financeiro['data_pagamento'] = financeiro['data_pagamento'].strftime('%d/%m/%Y') if financeiro['data_pagamento'] else None
                financeiro['data_vencimento'] = financeiro['data_vencimento'].strftime('%d/%m/%Y') if financeiro['data_vencimento'] else None

        else:
            financeiro_list = []

        # Verificar se a solicitação é AJAX e retornar JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'financeiros': financeiro_list})

        return render(request, 'financeiro.html', {'clientes': clientes_list,'financeiros': financeiro_list})


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
        valor_com_juros=data.get('valor_com_juros')
        valor_pago = data.get('valor_pago')



        cliente = get_object_or_404(Cliente, id=cliente_id)

        financeiro = Financeiro.objects.create(cliente=cliente,
                                               data_pagamento=data_pagamento,
                                               data_vencimento = data_vencimento,
                                               valor_mensalidade = valor_mensalidade,
                                               descricao_pagamento=descricao_pagamento,
                                               valor_com_juros=valor_com_juros,
                                               valor_pago=valor_pago)
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

def delete_financeiro(request, pagamento_id):
    if request.method == "DELETE":
        financeiro = get_object_or_404(Financeiro, id=pagamento_id)
        financeiro.delete()
        return JsonResponse({'message': 'Pagamento excluído com sucesso.'})
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

def comprovante_generator(request, pagamento_id):

    if request.method == "GET":

         # Coletar os dados do pagamento e do cliente
        dados_pagamento = Financeiro.objects.filter(id=pagamento_id).values(
            'id', 'cliente_id','data_pagamento', 'data_vencimento',
            'descricao_pagamento', 'valor_mensalidade', 'valor_com_juros', 'valor_pago', 
            'cliente__nome', 'cliente__cpf','cliente__datanascimento','cliente__email','cliente__endereco',
            'cliente__bairro','cliente__cep','cliente__cidade','cliente__estado','cliente__telefone',
            'cliente__celular','cliente__nome_responsavel','cliente__cpf_responsavel','cliente__nascimento_responsavel',
            'cliente__cursos','cliente__duracao','cliente__inicio','cliente__dias_curso','cliente__horarios_curso',
            'cliente__instrutor','cliente__mensalidade','cliente__parcelas','cliente__dia_pagamento','cliente__total',
        ).first()

        dados_pagamento['data_pagamento'] = dados_pagamento['data_pagamento'].strftime('%d/%m/%Y')
        dados_pagamento['data_vencimento'] = dados_pagamento['data_vencimento'].strftime('%d/%m/%Y')

        if not dados_pagamento:
            return HttpResponse('Pagamento não encontrado', status=404)

        # Criar o PDF
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = f'attachment; filename="comprovante_"{dados_pagamento['cliente__nome']}_{pagamento_id}".pdf"'

        logo = "templates\static\logo.jpg"
        carimbo = "templates\static\carimbo.png"

        width, height = A4
        pdf = canvas.Canvas(response, pagesize=A4)

        # Cabeçalho
        #ALTURA IMG 1.8 /LARGURA 5.5
        pdf.drawImage(logo, 2 * cm, 27.3 * cm, 5.5 * cm, 1.5 * cm, mask='auto')
        pdf.drawImage(carimbo, 12 * cm, 15*cm , 7 * cm , 3.5*cm, mask='auto')

        pdf.setFont("Helvetica", 10)
        pdf.drawString(8 * cm, height - 1.2 * cm, "SISTEMA DE CURSOS PROFISSIONALIZANTES LTDA")
        pdf.drawString(8 * cm, height - 1.7 * cm, "CNPJ: 02.946.004/0001-92")
        pdf.drawString(8 * cm, height - 2.2 * cm, "Rua Marte, 08 | Bairro Jardim Brasília | Uberlândia-MG | Fone: 3210-3324")
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(6 * cm, height - 3.2 * cm, "COMPROVANTE DE PAGAMENTO")
    
        # Dados do Aluno (Left)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 4 * cm, "Nome aluno:")
        pdf.drawString(5 * cm, height - 4 * cm, f"{dados_pagamento['cliente__nome']}")
        pdf.drawString(2 * cm, height - 4.5 * cm, "Endereço:")
        pdf.drawString(5 * cm, height - 4.5 * cm, f"{dados_pagamento['cliente__endereco']}")
        pdf.drawString(2 * cm, height - 5 * cm, "Cidade/ES:")
        pdf.drawString(5 * cm, height - 5 * cm, f"{dados_pagamento['cliente__cidade']}/{dados_pagamento['cliente__estado']}")

        pdf.drawString(2 * cm, height - 5.5 * cm, "Responsável:")
        pdf.drawString(5 * cm, height - 5.5 * cm, f"{dados_pagamento['cliente__nome_responsavel']}")
        pdf.drawString(2 * cm, height - 6 * cm, "E-mail:")
        pdf.drawString(5 * cm, height - 6 * cm, f"{dados_pagamento['cliente__email']}")
        
        # Dados do Aluno (Right)
        pdf.drawString(12 * cm, height - 4 * cm, "Código do aluno:")
        pdf.drawString(16 * cm, height - 4 * cm, f"{dados_pagamento['cliente_id']}")
        pdf.drawString(12 * cm, height - 4.5 * cm, "Bairro:")
        pdf.drawString(16 * cm, height - 4.5 * cm, "Jardim Brasília")
        pdf.drawString(12 * cm, height - 5 * cm, "CEP:")
        pdf.drawString(16 * cm, height - 5 * cm, f"{dados_pagamento['cliente__cep']}")
        pdf.drawString(12 * cm, height - 5.5 * cm, "Fone:")
        pdf.drawString(16 * cm, height - 5.5 * cm, f"{dados_pagamento['cliente__telefone']}")
        pdf.drawString(12 * cm, height - 6 * cm, "CPF:")
        pdf.drawString(16 * cm, height - 6 * cm, f"{dados_pagamento['cliente__cpf']}")

        # Detalhamento dos Cursos
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2 * cm, height - 7 * cm, "Detalhamento dos Cursos:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 7.5 * cm, f"{dados_pagamento['cliente__cursos']}")
        #pdf.drawString(2 * cm, height - 9 * cm, "Horário do Curso:")
        #pdf.drawString(5 * cm, height - 9 * cm, f"{dados_pagamento['cliente__dias_curso']} - {dados_pagamento['cliente__horarios_curso']}")
        
        # Detalhamento do pagamento
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2 * cm, height - 8.5 * cm, "Detalhamento do Pagamento:")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 9 * cm, "Mês de referência:")
        pdf.drawString(5 * cm, height - 9 * cm, f"{dados_pagamento['descricao_pagamento']}")
        pdf.drawString(12 * cm, height - 9 * cm, "Valor da mensalidade:")
        pdf.drawString(16 * cm, height - 9 * cm, f"{dados_pagamento['valor_mensalidade']}")

        pdf.drawString(2 * cm, height - 9.5 * cm, "Data vencimento:")
        pdf.drawString(5 * cm, height - 9.5 * cm, f"{dados_pagamento['data_vencimento']}")
        pdf.drawString(12 * cm, height - 9.5 * cm, "Valor com juros:")
        pdf.drawString(16 * cm, height - 9.5 * cm, f"{dados_pagamento['valor_com_juros']}")

        pdf.drawString(2 * cm, height - 10 * cm, "Data pagamento:")
        pdf.drawString(5 * cm, height - 10 * cm, f"{dados_pagamento['data_pagamento']}")
        pdf.drawString(12 * cm, height - 10 * cm, "Valor pago:")
        pdf.drawString(16 * cm, height - 10 * cm, f"{dados_pagamento['valor_pago']}")

        pdf.drawString(2 * cm, height - 10.5 * cm, "Dias em atraso:")
        pdf.drawString(5 * cm, height - 10.5 * cm, "95")
        pdf.drawString(12 * cm, height - 10.5 * cm, "Responsável pela venda:")
        pdf.drawString(16 * cm, height - 10.5 * cm, "_________________")

        # Assinatura
        pdf.drawString(2 * cm, height - 11.5 * cm, "E por ser verdade, assinam o presente.")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 13 * cm, "_______________________")
        pdf.drawString(2 * cm, height - 13.5 * cm, "Assinatura")

        #pdf.drawString(12 * cm, height - 13 * cm, "_______________________")
        #pdf.drawString(14 * cm, height - 14  * cm, "CARIMBO")
        
        
        ####
        pdf.drawString(2 * cm, height - 14.8  * cm, "-   -\
                                                            \
                                                             \
                                                        -   -")
        ####

        pdf.drawImage(logo, 2 * cm, 12.8 * cm, 5.5 * cm, 1.5 * cm, mask='auto')
        pdf.drawImage(carimbo, 12 * cm, 0.5*cm , 7 * cm , 3.5*cm, mask='auto')

        pdf.setFont("Helvetica", 10)
        pdf.drawString(8 * cm, height - 15.7 * cm, "SISTEMA DE CURSOS PROFISSIONALIZANTES LTDA")
        pdf.drawString(8 * cm, height - 16.2 * cm, "CNPJ: 02.946.004/0001-92")
        pdf.drawString(8 * cm, height - 16.7 * cm, "Rua Marte, 08 | Bairro Jardim Brasília | Uberlândia-MG | Fone: 3210-3324")
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(6 * cm, height - 17.7 * cm, "COMPROVANTE DE PAGAMENTO")
    
        # Dados do Aluno (Left)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 18.5 * cm, "Nome aluno:")
        pdf.drawString(5 * cm, height - 18.5 * cm, f"{dados_pagamento['cliente__nome']}")
        pdf.drawString(2 * cm, height - 19 * cm, "Endereço:")
        pdf.drawString(5 * cm, height - 19 * cm, f"{dados_pagamento['cliente__endereco']}")
        pdf.drawString(2 * cm, height - 19.5 * cm, "Cidade/ES:")
        pdf.drawString(5 * cm, height - 19.5 * cm, f"{dados_pagamento['cliente__cidade']}/{dados_pagamento['cliente__estado']}")

        pdf.drawString(2 * cm, height - 20 * cm, "Responsável:")
        pdf.drawString(5 * cm, height - 20 * cm, f"{dados_pagamento['cliente__nome_responsavel']}")
        pdf.drawString(2 * cm, height - 20.5 * cm, "E-mail:")
        pdf.drawString(5 * cm, height - 20.5 * cm, f"{dados_pagamento['cliente__email']}")
        
        # Dados do Aluno (Right)
        pdf.drawString(12 * cm, height - 18.5 * cm, "Código do aluno:")
        pdf.drawString(16 * cm, height - 18.5 * cm, f"{dados_pagamento['cliente_id']}")
        pdf.drawString(12 * cm, height - 19 * cm, "Bairro:")
        pdf.drawString(16 * cm, height - 19 * cm, "Jardim Brasília")
        pdf.drawString(12 * cm, height - 19.5 * cm, "CEP:")
        pdf.drawString(16 * cm, height - 19.5 * cm, f"{dados_pagamento['cliente__cep']}")
        pdf.drawString(12 * cm, height - 20 * cm, "Fone:")
        pdf.drawString(16 * cm, height - 20 * cm, f"{dados_pagamento['cliente__telefone']}")
        pdf.drawString(12 * cm, height - 20.5 * cm, "CPF:")
        pdf.drawString(16 * cm, height - 20.5 * cm, f"{dados_pagamento['cliente__cpf']}")

        # Detalhamento dos Cursos
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2 * cm, height - 21.5 * cm, "Detalhamento dos Cursos:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 22 * cm, f"{dados_pagamento['cliente__cursos']}")
        #pdf.drawString(2 * cm, height - 9 * cm, "Horário do Curso:")
        #pdf.drawString(5 * cm, height - 9 * cm, f"{dados_pagamento['cliente__dias_curso']} - {dados_pagamento['cliente__horarios_curso']}")
        
        # Detalhamento do pagamento
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(2 * cm, height - 23 * cm, "Detalhamento do Pagamento:")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 23.5 * cm, "Mês de referência:")
        pdf.drawString(5 * cm, height - 23.5 * cm, f"{dados_pagamento['descricao_pagamento']}")
        pdf.drawString(12 * cm, height - 23.5 * cm, "Valor da mensalidade:")
        pdf.drawString(16 * cm, height - 23.5 * cm, f"{dados_pagamento['valor_mensalidade']}")

        pdf.drawString(2 * cm, height - 24 * cm, "Data vencimento:")
        pdf.drawString(5 * cm, height - 24 * cm, f"{dados_pagamento['data_vencimento']}")
        pdf.drawString(12 * cm, height - 24 * cm, "Valor com juros:")
        pdf.drawString(16 * cm, height - 24 * cm, f"{dados_pagamento['valor_com_juros']}")

        pdf.drawString(2 * cm, height - 24.5 * cm, "Data pagamento:")
        pdf.drawString(5 * cm, height - 24.5 * cm, f"{dados_pagamento['data_pagamento']}")
        pdf.drawString(12 * cm, height - 24.5 * cm, "Valor pago:")
        pdf.drawString(16 * cm, height - 24.5 * cm, f"{dados_pagamento['valor_pago']}")

        pdf.drawString(2 * cm, height - 25 * cm, "Dias em atraso:")
        pdf.drawString(5 * cm, height - 25 * cm, "95")
        pdf.drawString(12 * cm, height - 25 * cm, "Responsável pela venda:")
        pdf.drawString(16 * cm, height - 25 * cm, "_________________")

        # Assinatura
        pdf.drawString(2 * cm, height - 26 * cm, "E por ser verdade, assinam o presente.")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 27.5 * cm, "_______________________")
        pdf.drawString(2 * cm, height - 28 * cm, "Assinatura")


        pdf.showPage()
        pdf.save()

        return response
    else:
        return HttpResponse('Método não permitido', status=405)