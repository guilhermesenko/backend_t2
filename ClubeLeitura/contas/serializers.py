'''
Serializers do app contas (usuários).
'''
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegistroSerializer(serializers.ModelSerializer):
    # A senha só entra (write_only) e passa pelos validadores do Django.
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, dados):
        usuario = User.objects.create_user(
            username=dados['username'],
            email=dados.get('email', ''),
            password=dados['password'],
        )
        return usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
