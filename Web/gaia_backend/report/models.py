from django.db import models
from authentication.models import Usuario

class Propriedade(models.Model):
    nome = models.CharField(max_length=200)
    localizacao = models.CharField(max_length=300)
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

class Laudo(models.Model):
    # APENAS os campos essenciais
    numero_amostra = models.IntegerField(verbose_name="Número da amostra")
    data_coleta = models.DateField(verbose_name="Data da coleta")
    
    # Apenas 1 campo de PDF
    arquivo_pdf = models.FileField(
        upload_to='laudos/pdf/', 
        verbose_name="PDF do Laudo"
    )
    
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Amostra {self.numero_amostra} - {self.data_coleta}"

    class Meta:
        verbose_name = 'Laudo'
        verbose_name_plural = 'Laudos'