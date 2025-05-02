from django.db import models

class Precos(models.IntegerChoices):
    TRIMESTRAL = 90, 'Trimestral - 90 dias (R$ 60,00)'
    SEMESTRAL = 180, 'Semestral - 180 dias (R$ 99,00)'
    ANUAL = 365, 'Anual - 365 dias (R$ 120,00)'

    @classmethod
    def get_repeats(cls, value):
        return {
            cls.TRIMESTRAL: 3,
            cls.SEMESTRAL: 6,
            cls.ANUAL: 12
        }.get(value)

    @classmethod
    def get_preco(cls, value):
        return {
            cls.TRIMESTRAL: 60,
            cls.SEMESTRAL: 99,
            cls.ANUAL: 120
        }.get(value)
    
    @classmethod
    def get_text(cls, value):
        return {
            cls.TRIMESTRAL: 'Trimestral - 90 dias',
            cls.SEMESTRAL: 'Semestral - 180 dias',
            cls.ANUAL: 'Anual - 365 dias'
        }.get(value)
    
class MetodoPagamento(models.TextChoices):
    CARTAO = 'credit_card', 'Cartão de Crédito'
    BOLETO = 'banking_billet', 'Boleto Bancário'

class StatusPagamento(models.TextChoices):
    PENDENTE = 'pendente', 'Pagamento Pendente'
    APROVADO = 'aprovado', 'Pagamento Aprovado'
    RECUSADO = 'recusado', 'Pagamento Recusado'
    ESTORNADO = 'estornado', 'Pagamento Estornado'
    REEMBOLSADO = 'reembolsado', 'Pagamento Reembolsado'