'''
Views do app contas: registro de novos usuários e identificação do usuário logado.
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from contas.serializers import RegistroSerializer, UsuarioSerializer


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
