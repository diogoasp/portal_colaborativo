from django.test import TestCase
from .models import Projeto, EtapasProjeto, Gerente, Stakeholder
from django.contrib.auth.models import User

class TestProjeto(TestCase):
    def setUp(self):
        self.projeto = Projeto.objects.create(nome='Meu Projeto', descricao='Descrição do Projeto', data_inicio=date.today(), data_fim=date.today() + timedelta(days=10), gerente=Gerente.objects.first())
        self.etapa1 = EtapasProjeto.objects.create(etapa='Etapa 1', projeto=self.projeto)
        self.etapa2 = EtapasProjeto.objects.create(etapa='Etapa 2', projeto=self.projeto)

    def test_visualizar_etapas(self):
        etapas = self.projeto.visualizar_etapas()
        self.assertIn(self.etapa1, etapas)
        self.assertIn(self.etapa2, etapas)

class ProjetoStakeholderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Projeto.objects.create(nome='Test Project', data_inicio='2022-01-01', gerente=self.user)
        self.stakeholder = Stakeholder.objects.create(usuario=self.user)

    def test_add_stakeholder(self):
        self.project.adicionar_stakeholder(self.stakeholder)
        self.assertTrue(self.stakeholder in self.project.stakeholders.all())

    def test_remove_stakeholder(self):
        self.project.adicionar_stakeholder(self.stakeholder)
        self.project.desligar_stakeholder(self.stakeholder)
        self.assertFalse(self.stakeholder in self.project.stakeholders.all())

class TestStakeholderMethods(TestCase):

    def setUp(self):
        self.gerente = Gerente(username='gerente1')
        self.projeto = Projeto(nome='Teste', gerente=self.gerente)
        self.stakeholder = Stakeholder(usuario=User(username='stakeholder1'))
        self.stakeholder.projetos.add(self.projeto)

    def test_solicitar_desligamento(self):
        self.stakeholder.solicitar_desligamento(self.projeto)
        self.assertTrue(self.gerente.notificar.called)
        expected_message = "O usuário stakeholder1 está solicitando desligamento do projeto Teste."
        self.assertEqual(self.gerente.notificar.call_args[0][0], expected_message)

if __name__ == '__main__':
    unittest.main()