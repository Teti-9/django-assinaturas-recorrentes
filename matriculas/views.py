import json
from django.views import View
from django.http import JsonResponse
from .forms import MatriculasForm, PagamentoForm, CancelarMatriculaForm
from .models import Pagamento, CancelarMatricula
from .responses import retornar_data
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class Matriculas(View):
    matriculas_form = MatriculasForm

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

@method_decorator(csrf_exempt, name='dispatch')
class Pagamentos(View):
    pagamento_form = PagamentoForm

    def get(self, request, id):
        pagamento = get_object_or_404(Pagamento, id=id)

        matricula = pagamento.pagamento

        response_data = retornar_data('pagamento', pagamento, matricula)

        return JsonResponse(response_data)

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
class CancelarMatriculas(View):
    cancelamento_form = CancelarMatriculaForm

    def get(self, request, id):
        cancelamento = get_object_or_404(CancelarMatricula, id=id)

        matricula = cancelamento.cancelamento

        response_data = retornar_data('cancelamento', cancelamento, matricula)

        return JsonResponse(response_data)

    def post(self, request):
        data = json.loads(request.body)
        form = self.cancelamento_form(data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                    'status': 'Success',
                    'message': 'Matrícula cancelada!',
                    'erros': form.errors,
                })
        
        return JsonResponse({
                'status': 'Error',
                'message': 'Dados inválidos!',
                'erros': form.errors,
            }, status=400)   