from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos adicionais ao usuário padrão do Django
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    
    # Define que o campo de login será o CPF em vez de username
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'email', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.cpf}"