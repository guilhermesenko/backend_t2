from django.contrib import admin
from livros.models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'ano', 'adicionado_por')
    search_fields = ('titulo', 'autor', 'genero')
    list_filter = ('genero', 'ano')
