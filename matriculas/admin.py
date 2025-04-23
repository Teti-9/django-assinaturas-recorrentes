from django.contrib import admin
from matriculas.models import Matricula, GerarPagamento, Pagamento

@admin.register(Matricula)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_do_plano', 'status_da_matricula', 'data_da_matricula', 'vencimento_da_matricula')
    exclude = ('plano', 'vencimento_da_matricula', 'status_da_matricula')

@admin.register(GerarPagamento)
class GerarPagamentosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'assinatura')
    exclude = ('assinatura',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pagamento', 'status_do_pagamento')
    exclude = ('status_do_pagamento',)