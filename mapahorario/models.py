from django.db import models

class Mapa(models.Model):

    horario = models.CharField(max_length=10)
    HSeg8comp_01 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_02 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_03 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_04 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_05 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_06 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_07 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_08 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_09 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_10 = models.CharField(max_length=100, blank=True, null=True)
    HSeg8comp_11 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.horario