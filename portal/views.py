from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Projeto, Interacao, Gerente
from .forms import ProjetoForm, InteracaoForm

class HomeView(ListView):
    template = 'home.html'
    def get(self,request):
        gerente = Gerente.objects.get(usuario=self.request.user)

        projetos = Projeto.objects.filter(gerente= gerente)
        interacoes = Interacao.objects.filter(estaAtiva=True, projeto__gerente=gerente)

        return render(request,'home.html',{'projetos':projetos, 'interacoes':interacoes})

# FBV para listar projetos
def lista_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, 'projeto/lista_projetos.html', {'projetos': projetos})

# CBV para detalhes do projeto
class ProjetoDetailView(DetailView):
    model = Projeto
    template_name = 'projeto/detalhes_projeto.html'
    context_object_name = 'projeto'

# Modifique a FBV para criar feedback para exigir login
# @login_required
# def criar_feedback(request, pk):
#     projeto = get_object_or_404(Projeto, pk=pk)
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.projeto = projeto
#             feedback.autor = request.user.stakeholder  # Assumindo que o usuário tem um perfil de stakeholder relacionado
#             feedback.save()
#             return redirect(projeto.get_absolute_url())  # Redireciona para a página de detalhes do projeto
#     else:
#         form = FeedbackForm()
#     return render(request, 'feedbacks/criar_feedback.html', {'form': form, 'projeto': projeto})

# Modifique a CBV para listar interações para exigir login
class InteracaoListView(LoginRequiredMixin, ListView):
    model = Interacao
    template_name = 'interacao/lista_interacoes.html'
    context_object_name = 'interacoes'

    def get_queryset(self):
        # Filtra as interações pelo projeto, se um 'projeto_id' for fornecido
        projeto_id = self.kwargs.get('projeto_id')
        if projeto_id:
            return Interacao.objects.filter(projeto__id=projeto_id)
        return Interacao.objects.all()
    
class ProjetoCreateView(CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto/projeto_form.html'
    success_url = reverse_lazy('lista_projetos')  # Substitua 'lista_projetos' pela URL de destino após a criação

class ProjetoUpdateView(UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto/projeto_form.html'
    success_url = reverse_lazy('lista_projetos')  # Substitua 'lista_projetos' pela URL de destino após a edição
  
class InteracaoCreateView(CreateView):
    model = Interacao
    form_class = InteracaoForm
    template_name = 'interacao/interacao_form.html'
    success_url = reverse_lazy('lista_interacoes')  # Substitua 'lista_interacoes' pela URL de destino após a criação

class InteracaoUpdateView(UpdateView):
    model = Interacao
    form_class = InteracaoForm
    template_name = 'interacao/interacao_form.html'
    success_url = reverse_lazy('lista_interacoes')  # Substitua 'lista_interacoes' pela URL de destino após a edição