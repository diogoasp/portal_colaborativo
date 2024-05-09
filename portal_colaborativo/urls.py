from django.urls import path
from django.contrib import admin
from portal import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('home', views.HomeView.as_view(), name='home'),
    path('projeto/novo/', views.ProjetoCreateView.as_view(), name='novo_projeto'),
    path('projeto/editar/<int:pk>/', views.ProjetoUpdateView.as_view(), name='editar_projeto'),
    path('projetos/', views.ProjetosView.as_view(), name='lista_projetos'),
    path('projetos/<int:pk>/', views.ProjetoDetailView.as_view(), name='detalhes_projeto'),
    # path('projetos/<int:pk>/feedback/', views.criar_feedback, name='criar_feedback'),
    path('interacoes/', views.InteracaoListView.as_view(), name='lista_interacoes'),
    path('interacao/nova/', views.InteracaoView.as_view(), name='nova_interacao'),
    path('interacao/editar/<int:pk>/', views.InteracaoView.as_view(), name='editar_interacao'),
    path('interacao/responder/<int:pk>/', views.ResponderInteracaoView.as_view(), name='responder_interacao'),
    # path('interacao/responder/', views.ResponderInteracaoView.as_view(), name='responder_interacao'),
]
