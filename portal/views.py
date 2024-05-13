from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Pergunta, Projeto, Interacao, Gerente, Resposta, Stakeholder
from .forms import ProjetoForm, InteracaoForm

class UserController():
    @classmethod
    def get_user(self, user):
        try:
            usuario = Gerente.objects.get(usuario=user)
        except Gerente.DoesNotExist:
            usuario = Stakeholder.objects.get(usuario=user)
        return usuario
    @classmethod
    def get_projects(self, user):
        print(user.__class__.__name__ )
        if user.__class__.__name__ == 'Stakeholder':
            projetos = Projeto.objects.filter(stakeholders=user)
        else:
            projetos = Projeto.objects.filter(gerente=user)
        return projetos
    @classmethod
    def get_interacoes(self, user):
        if user.__class__.__name__ == 'Stakeholder':
            interacoes = Interacao.objects.filter(estaAtiva=True, projeto__stakeholders=user)
        else:
            interacoes = Interacao.objects.filter(estaAtiva=True, projeto__gerente=user)
        return interacoes
    
class HomeView(ListView):
    template = 'home.html'
    def get(self,request):
        usuario = UserController.get_user(self.request.user)
        projetos = UserController.get_projects(usuario)
        interacoes = UserController.get_interacoes(usuario)

        return render(request,'home.html',{'projetos':projetos, 'interacoes':interacoes, 'usuario':usuario})

# FBV para listar projetos
class ProjetosView(LoginRequiredMixin,ListView):
    template = 'projeto/lista_projetos.html'
    def get(self,request):
        try:
            usuario = Gerente.objects.get(usuario=self.request.user)
        except Gerente.DoesNotExist:
            usuario = Stakeholder.objects.get(usuario=self.request.user)
        projetos = Projeto.objects.all()
        return render(request, self.template, {'projetos': projetos, 'usuario':usuario})

# CBV para detalhes do projeto
class ProjetoDetailView(DetailView):
    model = Projeto
    template_name = 'projeto/visualizar_projeto.html'
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

class InteracaoView(TemplateView):
    form = 'interacao/interacao_form.html'
    def get(self,request):
        interacao = InteracaoForm()
        return render(request, self.form, {'form': interacao})
    
    def post(self, request):
        interacao = InteracaoForm(request.POST)
        interacao.save()
        return redirect('home')

class ResponderInteracaoView(TemplateView):
    form = 'interacao/responder_interacao_form.html'
    def get(self, request, pk):
        interacao = get_object_or_404(Interacao, pk=pk)
        return render(request, self.form, {'form': interacao.formulario, 'pk':pk})
    
    def post(self, request, pk):
        interacao = Interacao.objects.get(pk=pk)
        stakeholder = Stakeholder.objects.get(usuario=self.request.user)
        pergunta = None
        resposta = []
        for key,value in request.POST.items():
            print(key,value)
            if key.split('-')[0] == 'question':
                pergunta = Pergunta.objects.create(pergunta=value)
            elif key.split('-')[0] == 'answer':
                resposta.append(Resposta.objects.create(interacao=interacao, pergunta=pergunta, stakeholder=stakeholder, resposta=value))

        return render(request, 'interacao/test.html', {'data': resposta})