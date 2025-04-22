from brutils import cpf, cep, phone, email
from brutils.cep import get_address_from_cep

def validar_cpf(value):
    if not cpf.is_valid(value):
        raise ValueError("CPF inválido")
        
def validar_cep(value):
    if not cep.is_valid(value):
        raise ValueError("CEP inválido")
    
def validar_telefone(value):
    if not phone.is_valid(value):
        raise ValueError("Telefone inválido")
    return phone.format_phone(value)

def validar_email(value):
    if not email.is_valid(value):
        raise ValueError("Email inválido")
    
def dados_residenciais(value):
    return get_address_from_cep(value)