from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def home(request):

    if  request.method == 'GET':

        return render(request, 'home.html')    
    
