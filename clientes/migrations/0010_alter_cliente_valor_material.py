# Generated by Django 5.0.6 on 2025-01-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_cliente_valor_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='valor_material',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
