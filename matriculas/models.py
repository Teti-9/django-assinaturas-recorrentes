from django.db import models, transaction
from django.utils import timezone
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
    
    assinatura = models.IntegerField(
        blank=True, 
        default=None, 
        verbose_name='assinatura_efi_id')
    
    data_da_matricula = models.DateTimeField(default=timezone.now)

    vencimento_da_matricula = models.DateTimeField(
        null=True, 
        blank=True)
    
    status_da_matricula = models.BooleanField(
        default=False)
    
    def __str__(self):
        return f"{self.aluno} - Matrícula: {self.id} - Plano: {Precos.get_text(Precos(self.tipo_do_plano))} - Valor: R${Precos.get_preco(Precos(self.tipo_do_plano))},00."

    def save(self, *args, **kwargs):
        if self.pk:
            old = type(self).objects.get(pk=self.pk)

        if not getattr(self, '_skip_assinatura', False):
            self.assinatura = assinatura_efi_id(plano_efi_id(self.tipo_do_plano), self.tipo_do_plano)

        if old.assinatura != self.assinatura:
            self.data_da_matricula = timezone.now()

        super().save(*args, **kwargs)

    def atualizar_vencimento_da_matricula(self):
        if self.vencimento_da_matricula is None:
            self.vencimento_da_matricula = self.data_da_matricula + timedelta(days=self.tipo_do_plano)

    def cancelar_matricula(self):
        with transaction.atomic():
            cancelar_assinatura(self.assinatura)
            self.vencimento_da_matricula = None
            self.status_da_matricula = False
            self._skip_assinatura = True
            self.save()
            del self._skip_assinatura

    class Meta:
        verbose_name_plural = "Matrículas"

class Pagamento(models.Model):
    pagamento = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE, 
        related_name='pagamento')
    
    status_do_pagamento = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="Pendente",
        verbose_name="status do pagamento")
    
    data_do_pagamento = models.DateTimeField(
        auto_now_add=True)
    
    def checar_aluno_matriculado(self, id):
        aluno = get_object_or_404(
            Alunos.objects.filter(matricula__assinatura__isnull=False),
            id=id
        )

        aluno_dict = model_to_dict(
            aluno,
            fields=['endereco_cep']
        )

        data = dados_residenciais(aluno_dict.get('endereco_cep'))
        return data
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            data = self.checar_aluno_matriculado(self.pagamento.aluno.id)

            pagar_assinatura(
                self.pagamento.assinatura, 
                data.get('logradouro'), 
                123, # Número fictício, pois não temos o número na API.
                data.get('bairro'), 
                remove_symbols(data.get('cep')), 
                data.get('localidade'), 
                data.get('complemento'), 
                data.get('uf'))
            
            self.atualizar_dados()

            self.pagamento._skip_assinatura = True
            self.pagamento.save()
            del self.pagamento._skip_assinatura

            super().save(*args, **kwargs)

    def atualizar_dados(self):
        self.status_do_pagamento = "Aprovado"
        self.data_do_pagamento = timezone.now()
        
        self.pagamento.status_da_matricula = True
        self.pagamento.atualizar_vencimento_da_matricula()

    def __str__(self):
        return f"{self.pagamento.aluno} - Plano: {Precos.get_text(Precos(self.pagamento.tipo_do_plano))} - Valor: R${Precos.get_preco(Precos(self.pagamento.tipo_do_plano))},00."
    
    class Meta:
        verbose_name_plural = "Pagamento"

class CancelarMatricula(models.Model):
    cancelamento = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE, 
        related_name='cancelamento')
    
    data_do_cancelamento = models.DateTimeField(
        auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.cancelamento.cancelar_matricula()

        self.data_do_cancelamento = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cancelamento.aluno}"

    class Meta:
        verbose_name_plural = "Cancelamento de Matrícula"