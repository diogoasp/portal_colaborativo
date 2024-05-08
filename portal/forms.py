from django import forms
from .models import *

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'gerente']
    def __init__(self, *args, **kwargs):
        super(ProjetoForm, self).__init__(*args, **kwargs)
        self.fields['data_inicio'].widget = forms.DateInput(attrs={'format':"dd/MM/yyyy", 'type': 'date'})
        self.fields['data_fim'].widget = forms.DateInput(attrs={'format':"dd/MM/yyyy", 'type': 'date'})

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['projeto','descricao','nome', 'estaAtiva']

