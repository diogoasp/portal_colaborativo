from django.urls import path
from portal import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('projeto/novo/', views.ProjetoCreateView.as_view(), name='novo_projeto'),
    path('projeto/editar/<int:pk>/', views.ProjetoUpdateView.as_view(), name='editar_projeto'),
    path('projetos/', views.lista_projetos, name='lista_projetos'),
    path('projetos/<int:pk>/', views.ProjetoDetailView.as_view(), name='detalhes_projeto'),
    path('projetos/<int:pk>/feedback/', views.criar_feedback, name='criar_feedback'),
    path('interacoes/', views.InteracaoListView.as_view(), name='lista_interacoes'),
    path('interacao/nova/', views.InteracaoCreateView.as_view(), name='nova_interacao'),
    path('interacao/editar/<int:pk>/', views.InteracaoUpdateView.as_view(), name='editar_interacao'),
]
