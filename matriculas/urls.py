from django.urls import path
from . import views

urlpatterns = [
    path('matricula', views.Matriculas.as_view(), name='cadastro_matricula'),
    path('matricula/<int:id>', views.Matriculas.as_view(), name='checar_matricula'),
    path('pagamento', views.Pagamentos.as_view(), name='pagamento'),
    path('cancelarmatricula', views.CancelarMatricula.as_view(), name='cancelar_matricula'),
]
