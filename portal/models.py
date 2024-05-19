from typing import Any
from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=255, null=False)
    dt_nascimento = models.DateField()
    contato = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
    def notificar(txt:str):
        pass

class NotificacaoUsuario(models.Model):
    mensagem = models.CharField(max_length=255, null=False, blank=False)
    dt_criacao = models.DateField(auto_created=True)

class Gerente(Usuario):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    def __str__(self):
        return self.usuario.get_full_name() or self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    gerente = models.ForeignKey(Gerente, on_delete=models.CASCADE)
    
    def visualizar_etapas(self):
        return self.etapas.all() 
    
    def adicionar_stakeholder(self, stakeholder):
        self.stakeholders.add(stakeholder)
    def desligar_stakeholder(self, stakeholder):
        self.stakeholders.remove(stakeholder)
    def __str__(self):
        return self.nome

class EtapasProjeto(models.Model):
    etapa = models.CharField(max_length=255)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='etapas')
    def __str__(self):
        return self.etapa

class Stakeholder(Usuario):
    projetos = models.ManyToManyField(Projeto, related_name='stakeholders')
    
    def __str__(self):
        return self.usuario.get_full_name() or self.nome

    def solicitar_desligamento(self, projeto:Projeto):
        projeto.gerente.notificar("O usuário %s está solicitando desligamento do projeto %s."%(self.nome, projeto.nome))

class Interacao(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='interacoes')
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=255)
    estaAtiva = models.BooleanField(default=True, null=False, blank=False, verbose_name="Interação Ativa")
    formulario = models.TextField()
    def __str__(self):
        return f'Interacao em {self.projeto.nome}'

class Pergunta(models.Model):
    pergunta = models.CharField(max_length=255)
	
class Resposta(models.Model):
    interacao = models.ForeignKey(Interacao, on_delete=models.CASCADE, related_name='respostas')
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('pergunta', 'stakeholder')

    def __str__(self):
        return f'Resposta de {self.stakeholder} para {self.interacao}'



    
    