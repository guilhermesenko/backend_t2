'''
Views do app leituras: lista de leituras pessoal de cada usuário.
Todos os endpoints exigem autenticação e operam apenas sobre as leituras do
próprio usuário logado.
'''
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from leituras.models import Leitura
from leituras.serializers import LeituraSerializer


class LeituraLista(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=LeituraSerializer(many=True),
                   summary='Lista as leituras do usuário logado')
    def get(self, request):
        leituras = Leitura.objects.filter(usuario=request.user)
        serializer = LeituraSerializer(leituras, many=True)
        return Response(serializer.data)

    @extend_schema(request=LeituraSerializer, responses=LeituraSerializer,
                   summary='Adiciona um livro à lista de leituras')
    def post(self, request):
        serializer = LeituraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeituraDetalhe(APIView):
    permission_classes = [IsAuthenticated]

    def get_objeto(self, request, pk):
        # Garante que o usuário só acessa as próprias leituras.
        return get_object_or_404(Leitura, pk=pk, usuario=request.user)

    @extend_schema(responses=LeituraSerializer, summary='Detalha uma leitura')
    def get(self, request, pk):
        leitura = self.get_objeto(request, pk)
        return Response(LeituraSerializer(leitura).data)

    @extend_schema(request=LeituraSerializer, responses=LeituraSerializer,
                   summary='Atualiza uma leitura')
    def put(self, request, pk):
        leitura = self.get_objeto(request, pk)
        serializer = LeituraSerializer(leitura, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Remove uma leitura')
    def delete(self, request, pk):
        leitura = self.get_objeto(request, pk)
        leitura.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
