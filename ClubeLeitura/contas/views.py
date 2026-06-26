'''
Views do app contas: registro de novos usuários, identificação do usuário logado
e gerência de senha (troca e redefinição via token).
'''
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from contas.serializers import (
    RegistroSerializer,
    UsuarioSerializer,
    TrocaSenhaSerializer,
    SolicitaResetSerializer,
    ConfirmaResetSerializer,
)


class Registro(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegistroSerializer, responses=UsuarioSerializer,
                   summary='Cria uma nova conta de usuário')
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(UsuarioSerializer(usuario).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuemSouEu(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UsuarioSerializer,
                   summary='Retorna os dados do usuário logado')
    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)


class TrocaSenha(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=TrocaSenhaSerializer,
                   summary='Troca a senha do usuário logado')
    def put(self, request):
        serializer = TrocaSenhaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        usuario = request.user
        if not usuario.check_password(serializer.validated_data['senha_atual']):
            return Response({'senha_atual': 'Senha atual incorreta.'},
                            status=status.HTTP_400_BAD_REQUEST)
        usuario.set_password(serializer.validated_data['senha_nova'])
        usuario.save()
        return Response({'detail': 'Senha alterada com sucesso.'})


class RecuperaSenha(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=SolicitaResetSerializer,
                   summary='Solicita a redefinição de senha (envia token por e-mail)')
    def post(self, request):
        serializer = SolicitaResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        usuario = User.objects.filter(email=email).first()
        # Só envia se o e-mail existir, mas a resposta é sempre a mesma para não
        # revelar quais e-mails estão cadastrados.
        if usuario:
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)
            send_mail(
                'Redefinição de senha - Clube de Leitura',
                f'Use os dados abaixo para redefinir sua senha.\n'
                f'uid: {uid}\ntoken: {token}',
                None,
                [email],
                fail_silently=True,
            )
        return Response({'detail': 'Se o e-mail existir, um token foi enviado.'})

    @extend_schema(request=ConfirmaResetSerializer,
                   summary='Confirma a redefinição de senha com uid, token e nova senha')
    def put(self, request):
        serializer = ConfirmaResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            pk = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            usuario = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'uid': 'Usuário inválido.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(usuario, serializer.validated_data['token']):
            return Response({'token': 'Token inválido ou expirado.'},
                            status=status.HTTP_400_BAD_REQUEST)
        usuario.set_password(serializer.validated_data['senha_nova'])
        usuario.save()
        return Response({'detail': 'Senha redefinida com sucesso.'})
