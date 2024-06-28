from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('faturamento/', include('faturamento.urls')),
    path('mapahorario/', include('mapahorario.urls')),
    path('historico/', include('historico.urls')),
    path('auth/', include('usuarios.urls')),
    path("", include('home.urls')),
    #path("", lambda request: redirect('/auth/login/'))

]
