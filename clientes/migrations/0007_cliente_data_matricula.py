# Generated by Django 5.0.6 on 2024-06-24 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_alter_cliente_situacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='data_matricula',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 6, 24, 8, 49, 29, 572894)),
        ),
    ]
