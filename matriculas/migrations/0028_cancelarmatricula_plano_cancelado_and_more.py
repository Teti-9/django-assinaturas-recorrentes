# Generated by Django 4.2.20 on 2025-05-08 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0027_alter_pagamento_status_do_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelarmatricula',
            name='plano_cancelado',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='plano cancelado'),
        ),
        migrations.AddField(
            model_name='pagamento',
            name='plano_pago',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='plano pago'),
        ),
    ]
