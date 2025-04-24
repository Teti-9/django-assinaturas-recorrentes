from django.contrib import admin
from matriculas.models import Matricula, Pagamento, CancelarMatricula

@admin.register(Matricula)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_do_plano', 'status_da_matricula', 'data_da_matricula', 'vencimento_da_matricula')
    exclude = ('assinatura', 'vencimento_da_matricula', 'status_da_matricula')

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pagamento', 'status_do_pagamento', 'data_do_pagamento')
    exclude = ('status_do_pagamento', 'data_do_pagamento')

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CancelarMatricula)
class CancelamentosAdmin(admin.ModelAdmin):
    list_display = ('cancelamento', 'data_do_cancelamento')
    exclude = ('data_do_cancelamento',)

    def has_delete_permission(self, request, obj=None):
        return False