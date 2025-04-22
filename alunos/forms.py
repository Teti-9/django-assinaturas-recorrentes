from django import forms
from .models import Alunos

class AlunosForm(forms.ModelForm):
    class Meta:
        model = Alunos
        fields = ['nome', 'cpf', 'email', 'data_de_nascimento', 'telefone', 'endereco_cep']