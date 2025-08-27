from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=255, blank=True, null=True) # blank=True e null=True tornam o campo opcional
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2) # Ex: SP, PR, etc.
    cep = models.CharField(max_length=9) # Formato 00000-000

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"

# Create your models here.
