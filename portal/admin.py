from django.contrib import admin
from .models import *

# Agora, registre os modelos com suas classes de administração personalizadas
admin.site.register(Projeto)
admin.site.register(EtapasProjeto)
admin.site.register(NotificacaoUsuario)
admin.site.register(Stakeholder)
admin.site.register(Gerente)
admin.site.register(Interacao)
admin.site.register(Resposta)