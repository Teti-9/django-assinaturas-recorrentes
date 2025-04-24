from django.contrib import admin
from .models import Alunos

@admin.register(Alunos)
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'data_de_nascimento', 'telefone', 'endereco_cep')

    def has_delete_permission(self, request, obj=None):
        return False