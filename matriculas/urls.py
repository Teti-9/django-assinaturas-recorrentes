from django.urls import path
from . import views

urlpatterns = [
    path('matricula', views.Matriculas.as_view(), name='cadastro_matricula'),
    path('matricula/<int:id>', views.Matriculas.as_view(), name='checar_matricula'),
    path('pagamento', views.Pagamentos.as_view(), name='pagamento'),
    path('pagamento/<int:id>', views.Pagamentos.as_view(), name='checar_pagamento'),
    path('cancelarmatricula', views.CancelarMatriculas.as_view(), name='cancelar_matricula'),
    path('cancelarmatricula/<int:id>', views.CancelarMatriculas.as_view(), name='checar_matricula_cancelada'),
]
