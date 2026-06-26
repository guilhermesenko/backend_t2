'''
Models do app livros - catálogo de livros do Clube de Leitura.
'''
from django.db import models
from django.contrib.auth.models import User


class Livro(models.Model):
    titulo    = models.CharField(max_length=200)
    autor     = models.CharField(max_length=120)
    genero    = models.CharField(max_length=80)
    ano       = models.IntegerField()
    descricao = models.TextField(blank=True)
    adicionado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='livros_adicionados',
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} ({self.autor})'
