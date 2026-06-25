from django.contrib import admin
from leituras.models import Leitura


@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'status', 'nota', 'data_adicionado')
    list_filter = ('status',)
    search_fields = ('usuario__username', 'livro__titulo')
