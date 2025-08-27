# gaia_backend/person/models.py

from django.db import models
from address.models import Address # Importa o modelo de Endereço da outra app

class Person(models.Model):
    # Campos herdados de Requester
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True) # unique=True garante que não haverá emails repetidos
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='people')

    # Campos próprios de Person
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=11, unique=True) # unique=True garante que não haverá CPFs repetidos

    def __str__(self):
        return self.name

# Create your models here.
