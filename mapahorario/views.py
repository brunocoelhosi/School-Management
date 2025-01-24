from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Mapa
from django.views.decorators.csrf import csrf_protect

@login_required(login_url = '/auth/login')
@csrf_protect
def mapahorario(request): 
    mapa = Mapa.objects.all()
    return render(request, 'mapahorario.html', {"schedule": mapa})

@csrf_protect
def update_schedule(request, pk, column):
    mapa = get_object_or_404(Mapa, pk=pk)
    new_value = request.POST.get("value", "")
    setattr(mapa, column, new_value)
    mapa.save()
    return HttpResponse(new_value)  # Retorna o novo valor para atualização em tempo real