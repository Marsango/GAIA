from django.db import models
from authentication.models import Usuario
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class Endereco(models.Model):
    cep = models.CharField(max_length=10, blank=True, null=True)
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    pais = models.CharField(max_length=255, default='Brasil')

    def __str__(self):
        if self.rua and self.numero:
            return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
        return f"{self.cidade}/{self.estado}"

class Person(models.Model):
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Empresa(models.Model):
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Propriedade(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.IntegerField(blank=True, null=True)
    localizacao = models.CharField(max_length=500, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    proprietario_pessoa = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.CASCADE
    )
    proprietario_empresa = models.ForeignKey(
        Empresa, null=True, blank=True, on_delete=models.CASCADE
    )
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.clean()  # Chama o método clean antes de salvar
        super().save(*args, **kwargs)

    def clean(self):
        if bool(self.proprietario_pessoa) == bool(self.proprietario_empresa):
            raise ValidationError(
                "A propriedade deve ter OU pessoa OU empresa como proprietária"
            )

    def __str__(self):
        return self.name
    
    @property
    def proprietario(self):
        """Retorna o proprietário (pessoa ou empresa) da propriedade"""
        return self.proprietario_pessoa or self.proprietario_empresa
    
    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

class Amostra(models.Model):
    numero_amostra = models.IntegerField()
    data_coleta = models.DateField()
    descricao = models.TextField(blank=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    
    # Parâmetros técnicos (campos do seu SQLite)
    area_total = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    profundidade = models.FloatField(null=True, blank=True)
    
    # Análise química
    fosforo = models.FloatField(null=True, blank=True)
    potassio = models.FloatField(null=True, blank=True)
    materia_organica = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    smp = models.FloatField(null=True, blank=True)
    aluminio = models.FloatField(null=True, blank=True)
    h_al = models.FloatField(null=True, blank=True)
    calcio = models.FloatField(null=True, blank=True)
    magnesio = models.FloatField(null=True, blank=True)
    cobre = models.FloatField(null=True, blank=True)
    ferro = models.FloatField(null=True, blank=True)
    manganes = models.FloatField(null=True, blank=True)
    zinco = models.FloatField(null=True, blank=True)
    soma_bases = models.FloatField(null=True, blank=True)
    ctc = models.FloatField(null=True, blank=True)
    v_percent = models.FloatField(null=True, blank=True)
    saturacao_aluminio = models.FloatField(null=True, blank=True)
    ctc_efetiva = models.FloatField(null=True, blank=True)
    
    # Análise física
    argila = models.FloatField(null=True, blank=True)
    silte = models.FloatField(null=True, blank=True)
    areia = models.FloatField(null=True, blank=True)
    classificacao = models.CharField(max_length=100, blank=True)
    
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Se não tiver usuário definido, usa o proprietário da propriedade
        if not self.usuario and self.propriedade:
            # Pega a pessoa ou empresa associada à propriedade
            if self.propriedade.proprietario_pessoa:
                self.usuario = self.propriedade.proprietario_pessoa
            elif self.propriedade.proprietario_empresa:
                # Se for empresa, não há usuário associado (diferente do modelo)
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Amostra {self.numero_amostra} - {self.propriedade.name}"
    

class Laudo(models.Model):
    numero_amostra = models.IntegerField()
    data_coleta = models.DateField()
    arquivo_pdf = models.FileField(upload_to='laudos/pdf/', blank=True, null=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laudo {self.numero_amostra} - {self.data_coleta}"