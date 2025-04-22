from django.contrib import admin
from matriculas.models import Matricula, GerarPagamento, Pagamento

@admin.register(Matricula)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_do_plano')
    exclude = ('plano', 'data_da_matricula', 'vencimento_da_matricula', 'status_da_matricula',)

@admin.register(GerarPagamento)
class PagamentosAdmin(admin.ModelAdmin):
    list_display = ('matricula',)
    exclude = ('assinatura',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pagamento',)
    exclude = ('status_do_pagamento',)