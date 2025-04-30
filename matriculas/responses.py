from django.forms.models import model_to_dict

def retornar_data(metodo: str, obj, matricula):
    tipo = {
        'cancelamento': 'data_do_cancelamento',
        'pagamento': 'data_do_pagamento'
    }

    data = getattr(obj, tipo[metodo])

    response_data = {
        f'{metodo}_id': obj.id,
        f'data_do_{metodo}': data,
        'matricula': {
            'id': matricula.id,
            'aluno': model_to_dict(matricula.aluno) if hasattr(matricula, 'aluno') else None,
            'tipo_do_plano': matricula.tipo_do_plano,
            'status_da_matricula': matricula.status_da_matricula,
            'vencimento_da_matricula': matricula.vencimento_da_matricula
        }
    }
    
    return response_data