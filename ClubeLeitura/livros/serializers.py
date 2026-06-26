'''
Serializers do app livros.
'''
from rest_framework import serializers
from livros.models import Livro


class LivroSerializer(serializers.ModelSerializer):
    # Mostra o username de quem cadastrou, sem permitir editar pelo corpo da requisição.
    adicionado_por = serializers.ReadOnlyField(source='adicionado_por.username')

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'genero', 'ano', 'descricao',
                  'adicionado_por', 'criado_em']
        read_only_fields = ['adicionado_por', 'criado_em']
