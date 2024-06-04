from django.db import models
from clientes.models import Cliente


class Financeiro(models.Model):

    #titulo = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    data_vencimento = models.DateField(null=True)
    valor_mensalidade = models.CharField(max_length=20)
    descricao_pagamento = models.CharField(max_length=50)
    data_pagamento = models.DateField(null=True)
    valor_com_juros = models.CharField(max_length=20)
    valor_pago = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.cliente_id) 
   
