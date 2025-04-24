import json
from django.views import View
from django.http import JsonResponse
from .forms import MatriculasForm, PagamentoForm, CancelarMatriculaForm
from .models import Alunos, Matricula
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict


@method_decorator(csrf_exempt, name='dispatch')
class Matriculas(View):
    matriculas_form = MatriculasForm

    def get(self, request, id):
        aluno = get_object_or_404(Alunos, id=id)

        aluno_dict = model_to_dict(
            aluno,
            fields=['nome', 'cpf', 'email', 'data_de_nascimento', 'telefone', 'endereco_cep']
        )

        if hasattr(aluno, 'matricula'):
            aluno_dict['matricula'] = model_to_dict(aluno.matricula,
                                                    fields=['aluno', 'tipo_do_plano', 'status_da_matricula'])
        else:
            aluno_dict['matricula'] = 'Nenhuma matrícula associada ao aluno.'

        return JsonResponse(aluno_dict)

    def post(self, request):
        data = json.loads(request.body)
        form = self.matriculas_form(data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Matrícula efetuada!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)
    
    def delete(self, request, id):
        obj = get_object_or_404(Matricula, id = id)
        
        obj.delete()
        
        return JsonResponse({
                'status': 'Success',
                'message': 'Matrícula deletada!'
            })  

@method_decorator(csrf_exempt, name='dispatch')
class Pagamentos(View):
    pagamento_form = PagamentoForm

    def post(self, request):
        data = json.loads(request.body)
        form = self.pagamento_form(data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Pagamento efetuado!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)
    
@method_decorator(csrf_exempt, name='dispatch')
class CancelarMatricula(View):
    cancelamento_form = CancelarMatriculaForm

    def post(self, request):
        data = json.loads(request.body)
        form = self.cancelamento_form(data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Pagamento gerado!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)   