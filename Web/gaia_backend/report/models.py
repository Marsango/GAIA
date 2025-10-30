from django.db import models
from authentication.models import Usuario

class Endereco(models.Model):
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    pais = models.CharField(max_length=255, default='Brasil')

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
    
class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Propriedade(models.Model):
    nome = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255)
    numero_registro = models.IntegerField(blank=True, null=True)
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

class Amostra(models.Model):
    numero_amostra = models.IntegerField()
    data_coleta = models.DateField()
    descricao = models.TextField(blank=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    
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

    def __str__(self):
        return f"Amostra {self.numero_amostra} - {self.propriedade.nome}"

class Laudo(models.Model):
    numero_amostra = models.IntegerField()
    data_coleta = models.DateField()
    arquivo_pdf = models.FileField(upload_to='laudos/pdf/')
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laudo {self.numero_amostra} - {self.data_coleta}"