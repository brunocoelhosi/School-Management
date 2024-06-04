from email.policy import default
from secrets import token_hex, token_urlsafe
from django.db import models
from clientes.models import Cliente
from .choices import ChoicesCategoriaManutencao
from datetime import datetime
from datetime import datetime
    

class CategoriaManutencao(models.Model):
    titulo = models.CharField(max_length=3, choices=ChoicesCategoriaManutencao.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.titulo

class Servico(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    categoria_manutencao = models.ManyToManyField(CategoriaManutencao)
    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    protocole = models.CharField(max_length=52, null=True, blank=True)
    identificador = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self) -> str:
        return self.titulo
    
