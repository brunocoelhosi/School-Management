from django.db import models

class Matricula(models.Model):

    nome_aluno = models.CharField(max_length=20)
    email_aluno = models.EmailField(max_length=50, blank=True)
    fone_aluno = models.CharField(max_length=20)
    nasc_aluno = models.DateField(null=True, blank=True)
    

    def __str__(self) -> str:
        return self.nome_aluno