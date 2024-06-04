from django.db import models

class Cliente(models.Model):
 
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=12, blank=False, null = False)
    datanascimento = models.DateField()
    email = models.EmailField()
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)

    nome_responsavel = models.CharField(max_length=50)
    cpf_responsavel = models.CharField(max_length=12)
    nascimento_responsavel = models.CharField(max_length=50)
    telefone_responsavel = models.CharField(max_length=50)

    cursos = models.CharField(max_length=50)
    duracao = models.CharField(max_length=50)
    inicio = models.CharField(max_length=50)

    dias_curso = models.CharField(max_length=50)
    horarios_curso = models.CharField(max_length=50)
    instrutor = models.CharField(max_length=50)
    mensalidade = models.CharField(max_length=50)
    parcelas = models.CharField(max_length=2)
    dia_pagamento = models.CharField(max_length=50)
    total = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome
