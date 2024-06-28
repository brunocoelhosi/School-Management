from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages, auth
from django.contrib.messages import constants
#from django.contrib.auth.models import User
from .models import Users

def cadastro(request):
    status = request.GET.get('status')
    return render(request,'cadastro.html', {'status': status})

def login(request):
    if request.user.is_authenticated:
        #messages.add_message(request, constants.SUCCESS, 'Login realizado com sucesso')
        return redirect ('/clientes/')
    status = request.GET.get('status')
    return render(request,'login.html', {'status':status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    if len(nome.strip()) == 0 or len(email.strip()) == 0: #se nome ou email for nulo, envia um cod erro
        messages.add_message(request, constants.WARNING, 'Nome e/ou Email inválidos.')
        return redirect('/auth/cadastro/')

    if len(senha)< 8:
        messages.add_message(request, constants.WARNING, 'A senha deve conter pelo menos 8 caracteres!') #senha < 8
        return redirect('/auth/cadastro/')

    if Users.objects.filter(email=email).exists(): #usuario ja existe
        messages.add_message(request, constants.ERROR, 'Email já cadastrado no sistema.') 
        return redirect('/auth/cadastro/')
    
    if Users.objects.filter(username=nome).exists(): #usuario ja existe
        messages.add_message(request, constants.ERROR, 'Usuário já cadastrado no sistema.') 
        return redirect('/auth/cadastro/')
    
    try:
        
        usuario = Users.objects.create_user(username = nome,
                                           email = email,
                                           password = senha)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        return redirect('/auth/cadastro/') #usuario cadastrado
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
        return redirect('/auth/cadastro/') #erro ao cadastrar

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
       
    usuario = auth.authenticate(request, username = nome, password = senha)

    if not usuario:
        messages.add_message(request, constants.WARNING, 'Usário ou Senha incorretos.')
        return redirect('/auth/login/') #nome ou senha incorreta

    else:
        auth.login(request, usuario)
        return redirect('/clientes/')
        
    #except:
        #messages.add_message(request, constants.WARNING, 'Faça o login antes de acessar o sistema.')
    #    return redirect('/auth/cadastro/') #erro ao logar
    
    
    
def sair(request):

    #request.session.flush() --- deleta session
    auth.logout(request)
    messages.add_message(request, constants.INFO, 'Logout realizado com sucesso.')
    return redirect('/auth/login/')
