from django.contrib import admin
from .models import Projeto, Feedback, Interacao


# Para uma personalização mais avançada, você pode criar classes de administração
# Isso permite definir como os modelos são exibidos na interface administrativa

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_inicio', 'data_fim')  # Ajuste os campos conforme necessário
    search_fields = ('nome', 'descricao')
    list_filter = ('data_inicio', 'data_fim')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'autor', 'conteudo', 'data_criacao')
    search_fields = ('conteudo', 'projeto__nome', 'autor__username')  # Ajuste conforme os modelos relacionados
    list_filter = ('data_criacao', 'projeto')

class InteracaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'projeto', 'data')
    search_fields = ('descricao', 'projeto__nome')
    list_filter = ('data', 'projeto')

# Agora, registre os modelos com suas classes de administração personalizadas
admin.site.register(Projeto)
admin.site.register(Feedback)
admin.site.register(Interacao)