from django import forms
from .models import Matricula, Pagamento, CancelarMatricula

class MatriculasForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'tipo_do_plano']

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pagamento']

class CancelarMatriculaForm(forms.ModelForm):
    class Meta:
        model = CancelarMatricula
        fields = ['cancelamento']