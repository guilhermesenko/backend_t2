'''
Rotas do app leituras.
'''
from django.urls import path
from leituras import views

urlpatterns = [
    path('', views.LeituraLista.as_view(), name='leitura_lista'),
    path('<int:pk>/', views.LeituraDetalhe.as_view(), name='leitura_detalhe'),
]
