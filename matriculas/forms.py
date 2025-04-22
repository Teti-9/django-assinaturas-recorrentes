from django import forms
from .models import Matricula, GerarPagamento, Pagamento

class MatriculasForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'tipo_do_plano']

class GerarPagamentosForm(forms.ModelForm):
    class Meta:
        model = GerarPagamento
        fields = ['matricula']

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pagamento']