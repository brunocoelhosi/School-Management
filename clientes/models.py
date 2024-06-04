from django.db import models

class Cliente(models.Model):
 
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=12, blank=False)
    datanascimento = models.DateField(null=True, blank=True)
    email = models.EmailField()
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=40)
    cep = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)

    nome_responsavel = models.CharField(max_length=50)
    cpf_responsavel = models.CharField(max_length=12)
    nascimento_responsavel = models.DateField(null=True, blank=True)
    telefone_responsavel = models.CharField(max_length=50)

    cursos = models.CharField(max_length=50)
    duracao = models.CharField(max_length=50)
    inicio = models.DateField(null=True, blank=True)

    dias_curso = models.CharField(max_length=50)
    horarios_curso = models.CharField(max_length=50)
    instrutor = models.CharField(max_length=50)
    mensalidade = models.CharField(max_length=50)
    parcelas = models.CharField(max_length=2)
    dia_pagamento = models.CharField(max_length=50)
    total = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.nome
