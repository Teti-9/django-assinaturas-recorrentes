from django.urls import path
from . import views

urlpatterns = [
    path('cadastro', views.Cadastro.as_view(), name='cadastro'),
    path('cadastro/<int:id>', views.Cadastro.as_view(), name='deletar_cadastro'),
]
