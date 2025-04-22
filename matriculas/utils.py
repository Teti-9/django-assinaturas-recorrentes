from efipay import EfiPay
from core.settings import EFI_CONFIG
from matriculas.enums import Precos

def plano_efi_id(plano):

    body_plan = {
        "name": 'Gym Membership', # Nome do plano.
        "interval": 1, # De quanto em quanto tempo será cobrado.
        "repeats": Precos.get_repeats(Precos(plano)), # Quantas vezes será cobrado.
    }

    response = EfiPay(EFI_CONFIG).create_plan(body=body_plan)
    return response['data']['plan_id']

def assinatura_efi_id(plano_id, plano):
    params = {
        'id': plano_id # ID do plano.
    }

    body = {
        "items": [
            {
                "name": "Assinatura recorrente academia",  # Nome do item.
                "value": Precos.get_preco(Precos(plano)) * 100, # Valor do item em centavos.
                "amount": 1 # Quantidade do item.
            }
        ]
    }

    response = EfiPay(EFI_CONFIG).create_subscription(params=params, body=body)
    return response['data']['subscription_id']

def pagar_assinatura(assinatura_id, rua, numero, bairro, cep, cidade, complemento, estado):
    params = {
    'id': assinatura_id  # ID da assinatura.
    }

    body = {
        "payment": {
            "credit_card": {
                "payment_token": "ca7573a520799d0b90f0d4be5c2c309b2ee4069b",
                "customer": {
                    "name": "Gorbadoc Oldbuck",
                    "cpf": "94271564656",
                    "email": "teste@gmail.com",
                    "birth": "2001-09-20",
                    "phone_number": "44999132273"
                },
                "billing_address": {
                    "street": rua,
                    "number": numero,
                    "neighborhood": bairro,
                    "zipcode": cep,
                    "city": cidade,
                    "complement": complemento,
                    "state": estado
                }
            }
        }
    }

    EfiPay(EFI_CONFIG).define_subscription_pay_method(params=params, body=body)

def cancelar_assinatura(assinatura_id):
    params = {
    'id': assinatura_id # ID da assinatura.
    }

    EfiPay(EFI_CONFIG).cancel_subscription(params=params)