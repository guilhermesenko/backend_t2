'''
Views do app livros: CRUD do catálogo.
Leitura liberada para todos; criação, edição e remoção só para administradores.
'''
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from livros.models import Livro
from livros.serializers import LivroSerializer
from livros.permissions import EhAdminOuSomenteLeitura


class LivroLista(APIView):
    permission_classes = [EhAdminOuSomenteLeitura]

    @extend_schema(responses=LivroSerializer(many=True),
                   summary='Lista os livros do catálogo')
    def get(self, request):
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)

    @extend_schema(request=LivroSerializer, responses=LivroSerializer,
                   summary='Cadastra um livro (somente admin)')
    def post(self, request):
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(adicionado_por=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LivroDetalhe(APIView):
    permission_classes = [EhAdminOuSomenteLeitura]

    @extend_schema(responses=LivroSerializer, summary='Detalha um livro')
    def get(self, request, pk):
        livro = get_object_or_404(Livro, pk=pk)
        return Response(LivroSerializer(livro).data)

    @extend_schema(request=LivroSerializer, responses=LivroSerializer,
                   summary='Atualiza um livro (somente admin)')
    def put(self, request, pk):
        livro = get_object_or_404(Livro, pk=pk)
        serializer = LivroSerializer(livro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Remove um livro (somente admin)')
    def delete(self, request, pk):
        livro = get_object_or_404(Livro, pk=pk)
        livro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
