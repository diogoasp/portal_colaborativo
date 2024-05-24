from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Pergunta, Projeto, Interacao, Gerente, Resposta, Stakeholder
from .forms import ProjetoForm, InteracaoForm, UserCreateForm
from django.contrib.auth.models import AnonymousUser
class UserController():
    @classmethod
    def get_user(self, user):
        if user is AnonymousUser:
            return None
        try:
            usuario = Gerente.objects.get(usuario=user)
        except Gerente.DoesNotExist:
            usuario = Stakeholder.objects.get(usuario=user)
        return usuario
    @classmethod
    def get_projects(self, user):
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
    
class HomeView(LoginRequiredMixin,ListView):
    template = 'home.html'
    def get(self,request):
        usuario = UserController.get_user(self.request.user)
        projetos = UserController.get_projects(usuario)
        interacoes = UserController.get_interacoes(usuario)
        context = {'projetos':projetos[0:5], 'interacoes':interacoes, 'usuario':usuario}
        if len(projetos) > 5:
            context['more'] = True
        return render(request,'home.html',context)

class ProjetosView(LoginRequiredMixin,ListView):
    template = 'projeto/lista_projetos.html'
    def get(self,request):
        usuario = UserController.get_user(self.request.user)
        projetos = UserController.get_projects(usuario)
        return render(request, self.template, {'projetos': projetos, 'usuario':usuario})

class ProjetoDetailView(LoginRequiredMixin,DetailView):
    model = Projeto
    template_name = 'projeto/visualizar_projeto.html'
    context_object_name = 'projeto'

class InteracaoListView(LoginRequiredMixin, TemplateView):
    model = Interacao
    template_name = 'interacao/lista_interacoes.html'

    def get(self, request, projeto_id=None):
        usuario = UserController.get_user(self.request.user)
        context = {'usuario': usuario}
        if projeto_id:
            context['interacoes'] = Interacao.objects.filter(projeto__id=projeto_id)
        else:
            context['interacoes'] = UserController.get_interacoes(usuario)
        return render(request, self.template_name, context)

class ProjetoCreateView(LoginRequiredMixin,CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto/projeto_form.html'
    success_url = reverse_lazy('lista_projetos')

class ProjetoUpdateView(LoginRequiredMixin,UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'projeto/projeto_form.html'
    success_url = reverse_lazy('lista_projetos')

class InteracaoView(LoginRequiredMixin,TemplateView):
    form = 'interacao/interacao_form.html'
    def get(self,request):
        interacao = InteracaoForm()
        return render(request, self.form, {'form': interacao})
    
    def post(self, request):
        interacao = InteracaoForm(request.POST)
        interacao.save()
        return redirect('home')

class ResponderInteracaoView(LoginRequiredMixin,TemplateView):
    form = 'interacao/responder_interacao_form.html'
    def get(self, request, pk):
        interacao = get_object_or_404(Interacao, pk=pk)
        return render(request, self.form, {'interacao':interacao, 'form': interacao.formulario, 'pk':pk})
    
    def post(self, request, pk):
        interacao = Interacao.objects.get(pk=pk)
        stakeholder = Stakeholder.objects.get(usuario=self.request.user)
        pergunta = None
        resposta = []
        for key,value in request.POST.items():
            if key.split('-')[0] == 'question':
                pergunta = Pergunta.objects.create(pergunta=value)
            elif key.split('-')[0] == 'answer':
                resposta.append(Resposta.objects.create(interacao=interacao, pergunta=pergunta, stakeholder=stakeholder, resposta=value))

        return render(request, 'interacao/test.html', {'stakeholder':stakeholder, 'interacao': interacao, 'data': resposta})

class ConstrucaoView(TemplateView):
    def get(self, request):
        return render(request, 'em_construcao.html')
    
class UserCreateView(TemplateView):
    def get(self, request):
        usuario = UserCreateForm()
        return render(request, 'usuario/cadastro_usuario.html', {'form': usuario})
    
    def post(self, request):
        usuario = UserCreateForm(request.POST)
        if usuario.is_valid():
            user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
            usuario.save()
            return redirect('home')
        else:
            return render(request, 'usuario/create_user_form.html', {'form': usuario})