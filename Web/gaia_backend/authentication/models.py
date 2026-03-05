from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)  # ← NOVO CAMPO
    
    # Campo novo para controlar o fluxo de primeiro acesso
    primeiro_acesso = models.BooleanField(default=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'email', 'first_name']

    def __str__(self):
        identifier = self.cpf or self.cnpj or 'sem-id'
        return f"{self.first_name} {self.last_name} - {identifier}"
    
class ConfiguracaoEmail(models.Model):
    assunto = models.CharField(max_length=200, default='Bem-vindo ao GAIA - Suas Credenciais')
    mensagem = models.TextField(default="""Olá {nome},

Seu cadastro no sistema GAIA foi realizado com sucesso.

Login: Seu {tipo_documento}
Sua senha temporária é:
{senha}

Por favor, altere sua senha no primeiro acesso.

Em caso de dúvidas, entre em contato com nosso suporte pelo numero (46)99999-9999 ou pelo email labsolos@gmail.com""")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Template de E-mail (Última edição: {self.updated_at})"

    class Meta:
        verbose_name = "Configuração de E-mail"
        verbose_name_plural = "Configurações de E-mail"


# ===============================================
# 🔐 RATE LIMITING PROGRESSIVO COM CAPTCHA
# ===============================================

class LoginAttempt(models.Model):
    """Rastreia tentativas de login para rate limiting progressivo"""
    identifier = models.CharField(max_length=20)  # CPF ou CNPJ
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "✅ Sucesso" if self.success else "❌ Falha"
        return f"{self.identifier} ({self.ip_address}) - {status}"
    
    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]


class CaptchaChallenge(models.Model):
    """Desafios CAPTCHA para usuários com múltiplas falhas"""
    identifier = models.CharField(max_length=20)  # CPF ou CNPJ
    ip_address = models.GenericIPAddressField()
    challenge_token = models.CharField(max_length=64, unique=True)
    challenge_key = models.CharField(max_length=10)  # ex: "3 + 5 = ?"
    correct_answer = models.CharField(max_length=10)  # ex: "8"
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_solved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"CAPTCHA: {self.identifier} - {self.challenge_key}"
    
    class Meta:
        indexes = [
            models.Index(fields=['challenge_token']),
            models.Index(fields=['expires_at']),
        ]
