from brutils import cpf, cep, phone, email
from brutils.cep import get_address_from_cep
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

def validar_cpf(value):
    if not cpf.is_valid(value):
        raise ValidationError("CPF Inválido. Digite o CPF sem pontos ou traços, exemplo: 82178537464")
    
def validar_email(value):
    if not email.is_valid(value):
        raise ValidationError("Email Inválido.")
    
def validar_telefone(value):
    if not phone.is_valid(value):
        raise ValidationError("Telefone Inválido. Digite o telefone sem parênteses ou traços, exemplo: 11994029275")
    return phone.format_phone(value)

def validar_cep(value):
    if not cep.is_valid(value):
        raise ValidationError("CEP Inválido. Digite o CEP sem traços, exemplo: 12345678")

def aluno_matriculado(id, model):
    aluno = get_object_or_404(
        model.objects.filter(matricula__assinatura__isnull=False),
        id=id
    )

    aluno_dict = model_to_dict(
        aluno,
        fields=['nome', 'email', 'cpf', 'data_de_nascimento', 'telefone', 'endereco_cep']
    )

    return aluno_dict