from django.db import models
from django.utils import timezone
from django.utils.timezone import now

class Matricula(models.Model):

    nome_aluno = models.CharField(max_length=20)
    email_aluno = models.EmailField(max_length=50, blank=True)
    fone_aluno = models.CharField(max_length=20)
    nasc_aluno = models.DateField(null=True, blank=True)

    data_pre = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return self.nome_aluno
    
    def save(self, *args, **kwargs):

        if not self.data_pre:
            self.data_pre = timezone.now()

        super().save(*args, **kwargs)
    