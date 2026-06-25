'''
Models do app leituras — lista de leituras pessoal de cada usuário.
'''
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from livros.models import Livro


class Leitura(models.Model):
    OPCOES_STATUS = [
        ('quero_ler', 'Quero Ler'),
        ('lendo',     'Lendo'),
        ('li',        'Li'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leituras')
    livro   = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='leituras')
    status  = models.CharField(max_length=10, choices=OPCOES_STATUS)
    nota    = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Nota de 1 a 5',
    )
    resenha = models.TextField(blank=True, help_text='Sua resenha do livro')
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'livro']
        ordering = ['-data_adicionado']

    def __str__(self):
        return f'{self.usuario.username} — {self.livro.titulo}'
