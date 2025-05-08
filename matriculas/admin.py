from django.contrib import admin
from matriculas.models import Matricula, Pagamento, CancelarMatricula

@admin.register(Matricula)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_do_plano', 'status_da_matricula', 'data_da_matricula', 'vencimento_da_matricula', 'assinatura', 'plano')
    exclude = ('plano', 'assinatura', 'vencimento_da_matricula', 'status_da_matricula', 'data_da_matricula')

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('plano_pago', 'status_do_pagamento', 'data_do_pagamento')
    exclude = ('status_do_pagamento', 'data_do_pagamento', 'plano_pago')

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj =None):
        return False

@admin.register(CancelarMatricula)
class CancelamentosAdmin(admin.ModelAdmin):
    list_display = ('plano_cancelado', 'data_do_cancelamento')
    exclude = ('data_do_cancelamento', 'plano_cancelado')

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj =None):
        return False