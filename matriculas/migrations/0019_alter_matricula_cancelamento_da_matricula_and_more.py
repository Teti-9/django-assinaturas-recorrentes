# Generated by Django 4.2.20 on 2025-04-23 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0018_alter_matricula_aluno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricula',
            name='cancelamento_da_matricula',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='vencimento_da_matricula',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
