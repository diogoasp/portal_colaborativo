from django import forms
from .models import Feedback, Projeto, Interacao

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['conteudo']

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'responsavel']

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['projeto', 'descricao']