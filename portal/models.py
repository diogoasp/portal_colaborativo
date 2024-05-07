from django.db import models
from django.contrib.auth.models import User

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    responsavel = models.ForeignKey(User, related_name='projetos_responsavel', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Stakeholder(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    projetos = models.ManyToManyField(Projeto, related_name='stakeholders')
    contato = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

class Feedback(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='feedbacks')
    autor = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='feedbacks')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Feedback por {self.autor} em {self.projeto}'

class TipoInteracao(models.Model):
    nome = models.CharField(max_length=255)
    def __str__(self):
        return f'Interacao em {self.nome}'

class Interacao(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='interacoes')
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(TipoInteracao, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Interacao em {self.projeto.nome}'

class InteracaoStakeholder(models.Model):
    interacao = models.ForeignKey(Interacao, on_delete=models.CASCADE)
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    resposta = models.TextField(null=True, blank=True)
    data_resposta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('interacao', 'stakeholder')
    
    def __str__(self):
        return f'Resposta de {self.stakeholder} para {self.interacao}'