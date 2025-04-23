from django.db import models
from alunos.models import Alunos
from matriculas.enums import Precos
from datetime import timedelta
from .utils import plano_efi_id, assinatura_efi_id, cancelar_assinatura, pagar_assinatura
from django.shortcuts import get_object_or_404
from alunos.utils import dados_residenciais
from django.forms.models import model_to_dict
from brutils.cep import remove_symbols

class Matricula(models.Model):
    aluno = models.OneToOneField(
        Alunos, 
        on_delete=models.CASCADE, 
        related_name='matricula')
    
    tipo_do_plano = models.IntegerField(
        choices=Precos.choices, 
        default=Precos.TRIMESTRAL, 
        help_text="Escolha seu plano.", 
        verbose_name="plano")
    
    plano = models.IntegerField(
        null=True, 
        blank=True, 
        default=None, 
        verbose_name='plano_efi_id')
    
    data_da_matricula = models.DateTimeField(
        auto_now_add=True)

    vencimento_da_matricula = models.DateField(
        null=True, 
        blank=True)
    
    status_da_matricula = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="Inativa",
        verbose_name="status da matrícula")
    
    def __str__(self):
        return f"{self.aluno} Plano: {Precos.get_text(Precos(self.tipo_do_plano))}."

    def save(self, *args, **kwargs):
        self.plano = plano_efi_id(self.tipo_do_plano)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if hasattr(self, 'gerar_pagamento') and self.gerar_pagamento.assinatura:
            cancelar_assinatura(self.gerar_pagamento.assinatura)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matrículas"

class GerarPagamento(models.Model):
    matricula = models.OneToOneField(
        Matricula,
        unique=True,
        on_delete=models.CASCADE, 
        related_name='gerar_pagamento')
    
    assinatura = models.IntegerField(
        null=True, 
        blank=True, 
        default=None, 
        verbose_name='assinatura_efi_id')
    
    def __str__(self):
        return f"{self.matricula}"

    def save(self, *args, **kwargs):
        if not self.pk:

            self.assinatura = assinatura_efi_id(self.matricula.plano, self.matricula.tipo_do_plano)

            super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Gerar Pagamento"


class Pagamento(models.Model):
    pagamento = models.OneToOneField(
        GerarPagamento,
        unique=True,
        on_delete=models.CASCADE, 
        related_name='pagamento')
    
    status_do_pagamento = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="Pendente",
        verbose_name="status do pagamento")
    
    @classmethod
    def checar_aluno_matriculado(cls, id):
        aluno = get_object_or_404(
            Alunos.objects.filter(matricula__gerar_pagamento__isnull=False),
            id=id
        )

        aluno_dict = model_to_dict(
            aluno,
            fields=['endereco_cep']
        )

        obj = dados_residenciais(aluno_dict.get('endereco_cep'))
        return [obj, aluno]
    
    def save(self, *args, **kwargs):
        if not self.pk:
            obj = Pagamento.checar_aluno_matriculado(self.pagamento.matricula.aluno.id)

            data = obj[0]
            aluno = obj[1]

            pagar_assinatura(
                aluno.matricula.gerar_pagamento.assinatura, 
                data.get('logradouro'), 
                123, # Número fictício, pois não temos o número na API.
                data.get('bairro'), 
                remove_symbols(data.get('cep')), 
                data.get('localidade'), 
                data.get('complemento'), 
                data.get('uf'))

            self.status_do_pagamento = "Aprovado"

            aluno.matricula.status_da_matricula = 'Ativa'

            aluno.matricula.vencimento_da_matricula = aluno.matricula.data_da_matricula + timedelta(days=aluno.matricula.tipo_do_plano)

            aluno.matricula.save()
            
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Pagamento"