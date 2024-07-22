from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import json
from clientes.models import Cliente
from financeiro.models import Financeiro

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_JUSTIFY

def historico(request):

    if request.method == "GET":

        id_teste = request.GET.get('id_js')
        print('id python:', id_teste)

        clientes_list = Cliente.objects.all()
        
        if id_teste:
            financeiro_list = list(Financeiro.objects.all().values('id', 'cliente_id', 'cliente__nome','data_pagamento',
                                                            'data_vencimento','descricao_pagamento','valor_mensalidade',
                                                            'valor_com_juros','valor_pago').filter(cliente_id=id_teste))
        else:   
            financeiro_list = []

        # Verificar se a solicitação é AJAX e retornar JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'financeiros': financeiro_list})
        
        return render(request, 'historico.html', {'clientes': clientes_list,'financeiros': financeiro_list})
    
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



def contrato_generator(request, clienteId):
    print(clienteId)
    if request.method == "GET":
        # Coletar os dados do pagamento e do cliente
        dados_pagamento = Cliente.objects.filter(id=clienteId).values(
            'id','nome', 'cpf','datanascimento','email','endereco',
            'bairro','cep','cidade','estado','telefone',
            'celular','nome_responsavel','cpf_responsavel','nascimento_responsavel',
            'cursos','duracao','inicio','dias_curso','horarios_curso',
            'instrutor','mensalidade','parcelas','dia_pagamento','total', 'situacao','data_matricula',
            'financeiro__id','financeiro__data_pagamento', 'financeiro__data_vencimento',
            'financeiro__descricao_pagamento', 'financeiro__valor_mensalidade', 'financeiro__valor_com_juros', 'financeiro__valor_pago',
        ).first()

        dados_pagamento['financeiro__data_pagamento'] = dados_pagamento['financeiro__data_pagamento'].strftime('%d/%m/%Y')
        dados_pagamento['financeiro__data_vencimento'] = dados_pagamento['financeiro__data_vencimento'].strftime('%d/%m/%Y')
        dados_pagamento['datanascimento'] = dados_pagamento['datanascimento'].strftime('%d/%m/%Y')
        dados_pagamento['inicio'] = dados_pagamento['inicio'].strftime('%d/%m/%Y')
        dados_pagamento['data_matricula'] = dados_pagamento['data_matricula'].strftime('%d de %B de %Y / %H:%Mh')

        if not dados_pagamento:
            return HttpResponse('Pagamento não encontrado', status=404)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprovante_{dados_pagamento["nome"]}.pdf"'
        
        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Desenhar logo e outras imagens
        logo = "templates/static/logo.jpg"  # Caminho para o logo
        pdf.drawImage(logo, 2 * cm, height - 2.2 * cm, 5.5 * cm, 1.5 * cm, mask='auto')

        # Adicionar informações do cabeçalho
        pdf.setFont("Helvetica", 9)
        pdf.drawString(8 * cm, height - 1 * cm, "SISTEMA DE CURSOS PROFISSIONALIZANTES LTDA")
        pdf.drawString(8 * cm, height - 1.5 * cm, "CNPJ: 02.946.004/0001-92")
        pdf.drawString(8 * cm, height - 2 * cm, "Rua Marte, 08 | Bairro Jardim Brasília | Uberlândia-MG | Fone: 3210-3324")
        pdf.setFont("Helvetica-Bold", 14)

        # Adicionar cláusulas do contrato
        styles = getSampleStyleSheet()



        # Estilo centralizado para o título
        centered_style = ParagraphStyle(
            'Centered',
            parent=styles['Normal'],
            fontSize=12,
            leading=12,
            alignment=1  # Centralizado
        )

        # Adicionar o título centralizado
        title = Paragraph("<b>TERMO DE COMPROMISSO</b><br/><br/>", centered_style)
        title_frame = Frame(2 * cm, height - 4.3 * cm, width - 4 * cm, 2 * cm, showBoundary=0)
        title_frame.addFromList([title], pdf)

        # Estilo para justificar o texto
        justified_style = ParagraphStyle(
            'Justified',
            parent=styles['Normal'],
            fontSize=8,
            leading=12,
            alignment=TA_JUSTIFY  # Justificar o texto
        )

        text = f"""
        O(a) Aluno(a): <b>{dados_pagamento["nome"]}</b>, Responsável: <b>{str(dados_pagamento['nome_responsavel'])}</b>, CPF: <b>{str(dados_pagamento['cpf'])}</b>,
          residente à: <b>{str(dados_pagamento['endereco'])}</b>, na cidade de <b>{str(dados_pagamento['cidade'])}/{str(dados_pagamento['estado'])}</b>,
            Fone: <b>{str(dados_pagamento['telefone'])}</b>. Email: <b>{str(dados_pagamento['email'])}</b>.<br/><br/>
        
        <b>Concordam nas seguintes cláusulas:</b><br/><br/>
        Aquisição dos cursos (módulos) de: <b>{str(dados_pagamento['cursos'])}</b><br/><br/>
        
        1. O SIS Informática se compromete em oferecer Qualidade Total na ministração dos cursos adquiridos pelo aluno com os seguintes benefícios:<br/>                                                                                                                                                                                                                                                                                                                                                                                                         
            <b>(I)</b> Experiência de mais de 26 anos de mercado em Uberlândia/MG e região. <b>(II)</b> Cursos de qualificação com instrutores habilitados,
              experiência comprovada e presentes em sala de aula. <b>(III)</b> Metodologia personalizada, material didático de qualidade, exercícios práticos
                correlacionados. <b>(IV)</b> Equipamentos adequados ao curso , infraestrutura moderna.<br/><br/>

        2. O Aluno se compromete a frequentar todas as aulas no horário agendado: <b>____________________</b> Na Unidade: <b>Jardim Brasilia</b>.<br/><br/>

        3. A duração dos cursos depende do DESEMPENHO, da FREQUÊNCIA e da PONTUALIDADE tendo uma previsão de <b>{str(dados_pagamento['duracao'])}</b> meses,
          com início em: <b>{str(dados_pagamento['inicio'])}</b>. Caso o aluno não conclua os módulos no tempo estipulado do contrato deverá continuar 
          com o pagamento das mensalidades pelo tempo necessário para o término.<br/><br/>

        4. O valor total do investimento é de <b>R$ {str(dados_pagamento['total'])}</b>, dividido em <b>{str(dados_pagamento['parcelas'])}</b> parcelas fixas de,
          <b>R$ {str(dados_pagamento['mensalidade'])}</b> ao mês, que deverá ser quitado no dia <b>{str(dados_pagamento['dia_pagamento'])}</b> de cada mês,
          sendo o primeiro pagamento em __________. O custo do material didático que será usado durante o curso é _______.
          Os juros pelo atraso do pagamento é de <b>R$ 0,33 ao dia. SENDO O DÉBIDO INSCRITO JUNTO AOS ÓRGÃOS
            DE PROTEÇÃO AO CRÉDITO (SERASA), após 30 dias do vencimento automaticamente.</b><br/>
            4.1. <b>APÓS 30 DIAS DE ATRASO DA MENSALIDADE AS AULAS SERÃO SUSPENSAS ATÉ O PAGAMENTO DA MESMA. A não frequência do aluno às aulas,
          não o isenta do pagamento das mensalidades, pois o horário fica reservado para o mesmo. </b> <br/><br/>
        
        5. Haverá reposição de aula quando o aluno tiver sido encaminhado para entrevista de emprego,
          houver apresentação de atestado médico ou falta de energia. No período de férias ou recesso o pagamento das mensalidades ocorre normalmente. 
          Não haverá reposição de feriados, férias e recessos. <br/><br/>

        6. Fica autorizado o uso e divulgação da imagem do aluno, concedida a título gratuito, abrangendo o uso da imagem em todo território nacional
          e no exterior, das seguintes formas: <b>(I)</b> out-door; <b>(II)</b> busdoor; folhetos em geral (encartes, mala direta, catálogo, etc.);
            <b>(III)</b> folder de apresentação; <b>(IV)</b> anúncios em revistas e jornais em geral; <b>(V)</b> home page; <b>(VI)</b> cartazes;
              <b>(VII)</b> mídia eletrônica (painéis, vídeos, televisão, cinema, rádio, entre outros). 
                Ainda autorizada, de livre e espontânea vontade, para os mesmos fins, a cessão de direitos da veiculação das imagens não recebendo 
                para tanto qualquer tipo de remuneração.<br/><br/>

        7. Para o aluno interromper o(s) curso(s) as mensalidades deverão estar em dia. 
        Havendo uma multa contratual de R$250,00 independente do(s) módulo(s) ainda não concluídos. 
        O aluno tem o direito de receber o certificado dos módulos 100% concluídos, desde que todas as parcelas, bem como a 
        multa contratual estejam devidamente quitados. <br/><br/>

        8.	No caso de cancelamento por parte do aluno, tendo já quitado o pacote de cursos e não feito, 
        o aluno deverá assinar o termo de cancelamento. Não haverá reembolso, a qualquer pretexto, dos valores já repassados ao SIS Cursos,
          após transcorridos os prazos legais para desistência. Tendo o direito de repassar o restante dos módulos para terceiros,
            em até 05 dias úteis após a notificação de desistência e assinatura do termo de cancelamento, devendo ser concluídos dentro do prazo e 
            carga horária do contrato original. <br/><br/>
            10.	A entrega do(s) Certificado(s) será uma semana após a conclusão do curso. A entrega estará condicionada a inexistência de débitos
              ou pendências do aluno junto ao SIS Cursos. Para emissão de 2ª Via de Certificado será cobrada taxa de R$ 20,00.<br/><br/>

        9.	E, por estarem em comum acordo, assinam o presente termo em 2 (duas) vias de igual teor.<br/><br/>

        Uberlândia/MG, <b>{str(dados_pagamento['data_matricula'])}</b><br/><br/>

        ____________________________________________<br/>
        Aluno(a): {str(dados_pagamento['nome'])}<br/><br/>

        ____________________________________________<br/>
        SISTEMA DE CURSOS PROFISSIONALIZANTES LTDA

        """
        pdf.drawString(12 * cm, height - 25.5 * cm, "_______________________")
        carimbo = "templates\static\carimbo.png"
        pdf.drawImage(carimbo, 12 * cm, 0.5*cm , 7 * cm , 3.5*cm, mask='auto')

        p = Paragraph(text, justified_style)
        frame = Frame(2 * cm, 1 * cm, width - 4 * cm, height - 4 * cm, showBoundary=0)
        frame.addFromList([p], pdf)

        pdf.save()
        return response
    else:
        return HttpResponse('Método não permitido', status=405)


def ficha_generator(request, clienteId):
    print(clienteId)
    if request.method == "GET":
        # Coletar os dados do pagamento e do cliente
        dados_pagamento = Cliente.objects.filter(id=clienteId).values(
            'id','nome', 'cpf','datanascimento','email','endereco',
            'bairro','cep','cidade','estado','telefone',
            'celular','nome_responsavel','cpf_responsavel','nascimento_responsavel',
            'cursos','duracao','inicio','dias_curso','horarios_curso',
            'instrutor','mensalidade','parcelas','dia_pagamento','total', 'situacao',
            'financeiro__id','financeiro__data_pagamento', 'financeiro__data_vencimento',
            'financeiro__descricao_pagamento', 'financeiro__valor_mensalidade', 'financeiro__valor_com_juros', 'financeiro__valor_pago',
        ).first()

        dados_pagamento['financeiro__data_pagamento'] = dados_pagamento['financeiro__data_pagamento'].strftime('%d/%m/%Y')
        dados_pagamento['financeiro__data_vencimento'] = dados_pagamento['financeiro__data_vencimento'].strftime('%d/%m/%Y')
        dados_pagamento['datanascimento'] = dados_pagamento['datanascimento'].strftime('%d/%m/%Y')
        dados_pagamento['inicio'] = dados_pagamento['inicio'].strftime('%d/%m/%Y')

        if not dados_pagamento:
            return HttpResponse('Pagamento não encontrado', status=404)

        # Configurações da página
        width, height = A4
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="Ficha_do_Instrutor.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.setTitle("Ficha do Instrutor")

        # Definir estilos
        styles = getSampleStyleSheet()
        normal = styles['Normal']

        # Cabeçalho
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(1.5 * cm, height - 1 * cm, f"CÓD.:{dados_pagamento['id']} {dados_pagamento['nome']}")
        
        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(10 * cm, height - 1 * cm, f"NASC.: {dados_pagamento['datanascimento']}")
        pdf.drawString(13.6 * cm, height - 1 * cm, f"FONE: {dados_pagamento['telefone']}")
        pdf.drawString(17 * cm, height - 1 * cm, f"DURAÇÃO: {dados_pagamento['duracao']}")
        
        pdf.setFillColor(colors.red)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(1.5 * cm, height - 1.5 * cm, f"DATA VENCIMENTO: {dados_pagamento['dia_pagamento']}")
        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(6.5 * cm, height - 1.5 * cm, f"RESP.: {dados_pagamento['nome_responsavel']}")
        pdf.drawString(12 * cm, height - 1.5 * cm, f"CURSOS: {dados_pagamento['cursos']}")
        

        # Seções de início, dias, horário e instrutor
        pdf.drawString(1.5 * cm, height - 2 * cm, f"DATA INÍCIO:___________")
        pdf.drawString(6.2 * cm, height - 2 * cm, "DIAS: ___________")
        pdf.drawString(9.8 * cm, height - 2 * cm, "HORÁRIO: ___________")
        pdf.drawString(14 * cm, height - 2 * cm, "INSTRUTOR (A): ____________")
        
        pdf.drawString(16 * cm, height - 3 * cm, "FALTAS")
        pdf.drawString(18 * cm, height - 3 * cm, "PGTO")
        #linhas
        pdf.line(15.9 * cm, height - 3.2 * cm, 15.9 * cm, height / 2) 
        pdf.line(17.7 * cm, height - 3.2 * cm, 17.7 * cm, height / 2)  
        pdf.line(19.3 * cm, height - 3.2 * cm, 19.3 * cm, height / 2)  

        pdf.save()
        return response
    else:
        return HttpResponse('Método não permitido', status=405)
