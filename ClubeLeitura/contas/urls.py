'''
Rotas do app contas.
'''
from django.urls import path
from contas import views

urlpatterns = [
    path('registrar/', views.Registro.as_view(), name='registro'),
    path('whoami/', views.QuemSouEu.as_view(), name='whoami'),
]
