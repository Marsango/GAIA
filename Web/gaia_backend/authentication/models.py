from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)  # ← NOVO CAMPO
    
    # Campo novo para controlar o fluxo de primeiro acesso
    primeiro_acesso = models.BooleanField(default=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'email', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.cpf}"
    
class ConfiguracaoEmail(models.Model):
    assunto = models.CharField(max_length=200, default='Bem-vindo ao GAIA - Suas Credenciais')
    mensagem = models.TextField(default="""Olá {nome},

Seu cadastro no sistema GAIA foi realizado com sucesso.

Suas credenciais de acesso são:
Login (CPF): {cpf}
Senha Temporária: {senha}

Por favor, altere sua senha no primeiro acesso.""")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Template de E-mail (Última edição: {self.updated_at})"

    class Meta:
        verbose_name = "Configuração de E-mail"
        verbose_name_plural = "Configurações de E-mail"