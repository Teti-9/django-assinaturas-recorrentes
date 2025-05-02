from django.db import models, transaction
from django.utils import timezone
from alunos.models import Alunos
from .services import AssinaturaService
from .exceptions import *
from matriculas.enums import Precos, MetodoPagamento, StatusPagamento
from datetime import timedelta
from alunos.utils import checar_aluno_matriculado

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
        blank=True, 
        default=None, 
        verbose_name='plano_efi_id')
    
    assinatura = models.IntegerField(
        blank=True, 
        default=None, 
        verbose_name='assinatura_efi_id')
    
    data_da_matricula = models.DateTimeField(
        auto_now_add=True)

    vencimento_da_matricula = models.DateTimeField(
        null=True, 
        blank=True)
    
    status_da_matricula = models.BooleanField(
        default=False)
    
    def __str__(self):
        return f"{self.aluno} - Matrícula: {self.id} - Plano: {Precos.get_text(Precos(self.tipo_do_plano))} - Valor: R${Precos.get_preco(Precos(self.tipo_do_plano))},00."

    def save(self, *args, **kwargs):
            
        try:
            with transaction.atomic():

                if self.pk:
                    self.data_da_matricula = timezone.now()

                plano_id, assinatura_id = AssinaturaService().criar_e_processar_assinatura(self.assinatura, self.tipo_do_plano)

                self.plano, self.assinatura = plano_id, assinatura_id
                
                super().save(*args, **kwargs)

        except AssinaturaExiste as e:
            error_msg = f"Já existe uma assinatura ativa ou pendente para {self.aluno}."
            raise AssinaturaExiste(error_msg) from e

        except ErroMatricula as e:
            print(f"Erro inesperado: {e}")

    class Meta:
        verbose_name_plural = "Matrículas"

class Pagamento(models.Model):
    pagamento = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE, 
        related_name='pagamento')
    
    status_do_pagamento = models.CharField(
        max_length=255,
        choices=StatusPagamento.choices,
        default=StatusPagamento.PENDENTE,
        help_text="Status do pagamento.",
        verbose_name="status do pagamento")
    
    metodo_do_pagamento = models.CharField(
        max_length=255,
        choices=MetodoPagamento.choices,
        default=MetodoPagamento.CARTAO,
        help_text="Escolha o método de pagamento.",
        verbose_name="metodo do pagamento")
    
    data_do_pagamento = models.DateTimeField(
        auto_now_add=True)
    
    def save(self, *args, **kwargs):

        data = checar_aluno_matriculado(self.pagamento.aluno.id, Alunos)

        try:
            with transaction.atomic():

                AssinaturaService().pagar_assinatura(self.pagamento.assinatura, self.metodo_do_pagamento, data, 123)
            
                Matricula.objects.filter(pk=self.pagamento.pk).update(
                    status_da_matricula = True,
                    vencimento_da_matricula = self.pagamento.data_da_matricula + timedelta(days=self.pagamento.tipo_do_plano)
                )

                self.status_do_pagamento = StatusPagamento.APROVADO

                super().save(*args, **kwargs)
            
        except ErroPagamento as e:
            error_msg = "Não é possível pagar esta assinatura."
            raise ErroPagamento(error_msg) from e
            
        except ErroMatricula as e:
            print(f"Erro inesperado: {e}")

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

        try:
            with transaction.atomic():

                AssinaturaService().cancelar_assinatura(self.cancelamento.assinatura)

                Matricula.objects.filter(pk=self.cancelamento.pk).update(
                    status_da_matricula = False,
                    vencimento_da_matricula = None,
                )

                self.status_da_matricula = False
                self.vencimento_da_matricula = None

                super().save(*args, **kwargs)

        except AssinaturaCancelada as e:
            error_msg = f"A assinatura com o plano {Precos.get_text(Precos(self.cancelamento.tipo_do_plano))} para {self.cancelamento.aluno}, já está cancelada."
            raise AssinaturaCancelada(error_msg) from e

        except ErroMatricula as e:
            print(f"Erro inesperado: {e}")

    def __str__(self):
        return f"{self.cancelamento.aluno}"

    class Meta:
        verbose_name_plural = "Cancelamento de Matrícula"