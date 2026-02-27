from django.contrib import admin
from .models import Propriedade, Laudo, Amostra, Empresa, Endereco

@admin.register(Propriedade)
class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('name', 'proprietario_pessoa', 'proprietario_empresa', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('name', 'registration_number')
    readonly_fields = ('data_cadastro',)
    ordering = ('-data_cadastro',)
    # list_editable = ('ativo',)

@admin.register(Amostra)
class AmostraAdmin(admin.ModelAdmin):
    list_display = ('numero_amostra', 'propriedade', 'data_coleta', 'ph', 'fosforo', 'potassio', 'ativo')
    list_filter = ('ativo', 'data_coleta', 'propriedade')
    search_fields = ('numero_amostra', 'propriedade__name', 'descricao')
    date_hierarchy = 'data_coleta'
    readonly_fields = ('data_cadastro',)

@admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
    list_display = ('numero_amostra', 'propriedade', 'data_coleta', 'ativo')
    list_filter = ('ativo', 'data_coleta')
    search_fields = ('numero_amostra', 'propriedade__name')
    readonly_fields = ('data_criacao',)
    # list_editable = ('ativo',)
    
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'telefone')
    search_fields = ('name', 'cnpj', 'email')
    
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'numero', 'cidade', 'estado', 'cep')
    search_fields = ('rua', 'cidade', 'estado', 'cep')   
