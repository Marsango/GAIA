from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuario

class EmailRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register-client')

    def test_register_sends_email(self):
        """Teste se ao registrar, um email é enviado com a senha"""
        data = {
            'email': 'teste@exemplo.com',
            'cpf': '123.456.789-00',
            'first_name': 'Bruno',
            'last_name': 'Marsango'
        }

        response = self.client.post(self.register_url, data)

        if response.status_code != 201:
            print("\n=== ERRO DETALHADO ===")
            print(response.data)
            print("======================\n")
        
        # Verifica se criou com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o usuário foi criado no banco
        user = Usuario.objects.get(email='teste@exemplo.com')
        self.assertTrue(user.primeiro_acesso) # Deve ser True por padrão

        # Verifica se 1 email foi enviado
        self.assertEqual(len(mail.outbox), 1)
        
        # Verifica o assunto do email
        self.assertEqual(mail.outbox[0].subject, 'Bem-vindo ao GAIA - Suas Credenciais')
        
        # Verifica se a senha (aleatória) está no corpo do email
        self.assertIn('Senha Temporária:', mail.outbox[0].body)