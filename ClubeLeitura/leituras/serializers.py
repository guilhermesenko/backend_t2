'''
Serializers do app leituras.
'''
from rest_framework import serializers
from leituras.models import Leitura
from livros.serializers import LivroSerializer


class LeituraSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    # Dados completos do livro (somente leitura); para gravar usa-se o campo 'livro'.
    livro_detalhe = LivroSerializer(source='livro', read_only=True)

    class Meta:
        model = Leitura
        fields = ['id', 'usuario', 'livro', 'livro_detalhe', 'status',
                  'nota', 'resenha', 'data_adicionado']
        read_only_fields = ['usuario', 'data_adicionado']

    def validate(self, dados):
        # Mesma regra do Trab1: nota e resenha só quando o status for 'li'.
        status = dados.get('status') or getattr(self.instance, 'status', None)
        nota = dados.get('nota', getattr(self.instance, 'nota', None))
        resenha = dados.get('resenha', getattr(self.instance, 'resenha', None))
        if status != 'li':
            if nota is not None:
                raise serializers.ValidationError(
                    {'nota': 'Só é possível dar nota depois de ler o livro.'})
            if resenha:
                raise serializers.ValidationError(
                    {'resenha': 'Só é possível escrever resenha depois de ler o livro.'})
        return dados
