import json
from django.views import View
from django.http import JsonResponse
from .forms import AlunosForm
from .models import Alunos
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

@method_decorator(csrf_exempt, name='dispatch')
class Cadastro(View):
    alunos_form = AlunosForm

    def get(self, request, id):
        aluno = get_object_or_404(Alunos, id=id)

        aluno_dict = model_to_dict(
            aluno,
            fields=['nome', 'cpf', 'email', 'data_de_nascimento', 'telefone', 'endereco_cep']
        )

        if hasattr(aluno, 'matricula'):
            aluno_dict['matricula'] = {
                **model_to_dict(
                    aluno.matricula,
                    fields=['aluno', 'tipo_do_plano', 'status_da_matricula', 'vencimento_da_matricula']
                ),
                'data_da_matricula': aluno.matricula.data_da_matricula
            }
        else:
            aluno_dict['matricula'] = 'Nenhuma matrícula associada ao aluno.'

        return JsonResponse(aluno_dict)

    def post(self, request):
        data = json.loads(request.body)
        form = self.alunos_form(data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Cadastro efetuado!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)
    
    def put(self, request, id):
        data = json.loads(request.body)
        obj = get_object_or_404(Alunos, id = id)

        form = self.alunos_form(data, instance=obj)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Aluno editado!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)
    
    def delete(self, request, id):
        obj = get_object_or_404(Alunos, id = id)
        
        obj.delete()
        
        return JsonResponse({
                'status': 'Success',
                'message': 'Aluno deletado!'
            })