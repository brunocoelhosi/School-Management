from django.shortcuts import render
from django.http import HttpResponse

def mapahorario(request): 
    return render(request, 'mapahorario.html')