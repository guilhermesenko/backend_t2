'''
Rotas do app livros.
'''
from django.urls import path
from livros import views

urlpatterns = [
    path('', views.LivroLista.as_view(), name='livro_lista'),
    path('<int:pk>/', views.LivroDetalhe.as_view(), name='livro_detalhe'),
]
