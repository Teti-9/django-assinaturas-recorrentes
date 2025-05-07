from django.utils import timezone
from dateutil.relativedelta import relativedelta
from efipay import EfiPay
from core.settings import EFI_CONFIG
from matriculas.enums import Precos
from brutils.cep import remove_symbols, get_address_from_cep
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
    
    def pagar_assinatura(self, assinatura_id, pagamento, data, numero):

        body = self._metodo_de_pagamento_cartao(data, numero) if pagamento == 'credit_card' else self._metodo_de_pagamento_boleto(data)
        
        status = self._assinatura_status(assinatura_id)

        if status == 'new':
            params = {
            'id': assinatura_id  # ID da assinatura.
            }

            response = self.efi.define_subscription_pay_method(params=params, body=body)

            if response.get('code') == 3500034: # Algum erro de validação.
                raise ErroPagamento("Não é possível pagar esta assinatura.")
            
            return True

        raise ErroPagamento("Não é possível pagar esta assinatura.")
    
    def cancelar_assinatura(self, assinatura_id):
        status = self._assinatura_status(assinatura_id)

        if status != 'canceled':
            params = {
            'id': assinatura_id # ID da assinatura.
            }

            self.efi.cancel_subscription(params=params)
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
                    "name": "Assinatura Recorrente",  # Nome do item.
                    "value": Precos.get_preco(Precos(self.plano)) * 100, # Valor do item em centavos.
                    "amount": 1 # Quantidade do item.
                }
            ]
        }

        response = self.efi.create_subscription(params=params, body=body)
        return response['data']['subscription_id']
        
    def _metodo_de_pagamento_cartao(self, data, numero):

        endereco = get_address_from_cep(data.get('endereco_cep'))
        
        body = {
            "payment": {
                'credit_card': {
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
    
    def _metodo_de_pagamento_boleto(self, data):

        body = {
            'payment': {
                'banking_billet': {
                    'expire_at': (timezone.now() + relativedelta(months=1)).strftime('%Y-%m-%d'),
                    'customer': {
                        'name': f'{data.get("nome")}',
                        'email': f'{data.get("email")}',
                        'cpf': f'{data.get("cpf")}',
                        'birth': f'{data.get("data_de_nascimento")}',
                        'phone_number': f'{data.get("telefone")}',
                    }
                }
            }
        }

        return body
    
    def _assinatura_status(self, assinatura_id):
        params = {
        'id': assinatura_id # ID da assinatura.
        }

        response = self.efi.detail_subscription(params=params)

        if response.get("code") == 3500034:
            return 'ok' # -> Cenário onde não existe assinatura prévia (Matrícula sendo criada.)

        return response['data']['status']
    
    def _assinatura_plano(self, assinatura_id):
        params = {
        'id': assinatura_id # ID da assinatura.
        }

        response = self.efi.detail_subscription(params=params)
        return response['data']['plan']['plan_id']