from efipay import EfiPay
from core.settings import EFI_CONFIG
from matriculas.enums import Precos
from brutils.cep import remove_symbols
from .exceptions import *

class AssinaturaService:
    def __init__(self):
        self.efi = EfiPay(EFI_CONFIG)
        self.plano = None
        self.valor = None
        self.assinatura = None

    def criar_e_processar_assinatura(self, assinatura, plano):
        status = self._assinatura_status(assinatura)
        
        if status == 'canceled' or status == 'ok':
            self.plano = plano
            plano_id = self._criar_plano(plano)
            assinatura_id = self._criar_assinatura(plano_id)
            
            return (plano_id, assinatura_id)
        
        raise AssinaturaExiste("Já existe uma assinatura ativa para este usuário")
    
    def pagar_assinatura(self, assinatura_id, pagamento, endereco, numero):
        body = self._metodo_de_pagamento(pagamento, endereco, numero)
        status = self._assinatura_status(assinatura_id)

        if status == 'new':
            params = {
            'id': assinatura_id  # ID da assinatura.
            }

            EfiPay(EFI_CONFIG).define_subscription_pay_method(params=params, body=body)
            return True

        raise ErroPagamento("Não é possível pagar esta assinatura.")
    
    def cancelar_assinatura(self, assinatura_id):
        status = self._assinatura_status(assinatura_id)

        if status != 'canceled':
            params = {
            'id': assinatura_id # ID da assinatura.
            }

            EfiPay(EFI_CONFIG).cancel_subscription(params=params)
            return True

        raise AssinaturaCancelada("Essa assinatura já está cancelada.")
    
    def _criar_plano(self, plano):
        body_plan = {
            "name": f'Plano Academia - {Precos.get_text(Precos(plano))}', # Nome do plano.
            "interval": 1, # De quanto em quanto tempo será cobrado.
            "repeats": Precos.get_repeats(Precos(plano)), # Quantas vezes será cobrado.
        }

        response = self.efi.create_plan(body=body_plan)
        return response['data']['plan_id']
    
    def _criar_assinatura(self, plano_id):
        params = {
            'id': plano_id # ID do plano.
        }

        body = {
            "items": [
                {
                    "name": "Assinatura recorrente academia",  # Nome do item.
                    "value": Precos.get_preco(Precos(self.plano)) * 100, # Valor do item em centavos.
                    "amount": 1 # Quantidade do item.
                }
            ]
        }

        response = EfiPay(EFI_CONFIG).create_subscription(params=params, body=body)
        return response['data']['subscription_id']
        
    def _metodo_de_pagamento(self, pagamento, endereco, numero):
        body = {
            "payment": {
                f"{pagamento}": {
                    "payment_token": "ca7573a520799d0b90f0d4be5c2c309b2ee4069b",
                    "customer": {
                        "name": "Gorbadoc Oldbuck",
                        "cpf": "94271564656",
                        "email": "teste@gmail.com",
                        "birth": "2001-09-20",
                        "phone_number": "44999132273"
                    },
                    "billing_address": {
                        "street": endereco.get('logradouro'),
                        "number": numero,
                        "neighborhood": endereco.get('bairro'),
                        "zipcode": remove_symbols(endereco.get('cep')),
                        "city": endereco.get('localidade'),
                        "complement": endereco.get('complemento'),
                        "state": endereco.get('uf')
                    }
                }
            }
        }

        return body
    
    def _assinatura_status(self, assinatura_id):
        params = {
        'id': assinatura_id # ID da assinatura.
        }

        response = EfiPay(EFI_CONFIG).detail_subscription(params=params)

        if response.get("code") == 3500034:
            return 'ok' # -> Cenário onde não existe assinatura prévia (Matrícula sendo criada.)

        return response['data']['status']
    
    def _assinatura_plano(self, assinatura_id):
        params = {
        'id': assinatura_id # ID da assinatura.
        }

        response = EfiPay(EFI_CONFIG).detail_subscription(params=params)
        return response['data']['plan']['plan_id']