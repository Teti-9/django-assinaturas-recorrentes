from django.db import models
from .utils import validar_cpf, validar_cep, validar_telefone, validar_email

class Alunos(models.Model):
    nome = models.CharField(
        max_length=255, 
        verbose_name="Nome do Aluno")
    
    cpf = models.CharField(
        max_length=11,
        default=None,
        unique=True,
        validators=[validar_cpf],
        help_text='Digite o CPF sem pontos ou traços, exemplo: 82178537464',
        verbose_name="CPF")
    
    email = models.EmailField(
        max_length=255, 
        default=None,
        validators=[validar_email], 
        help_text='Use o formato email@email.com', 
        verbose_name="Email")
    
    data_de_nascimento = models.DateField(
        default=None,
        help_text='Selecione sua data de nascimento.', 
        verbose_name="Data de Nascimento")
    
    telefone = models.CharField(
        max_length=11,
        default=None,
        validators=[validar_telefone],
        help_text='Digite o telefone sem parênteses ou traços, exemplo: 11994029275', 
        verbose_name="Telefone")

    endereco_cep = models.CharField(
        max_length=8,
        default=None,
        validators=[validar_cep],
        help_text='Digite o CEP sem traços, exemplo: 12345678',
        verbose_name="CEP"
    )
    
    def __str__(self):
        return f"{self.nome} (ID: {self.id})"

    class Meta:
        verbose_name_plural = "Alunos"