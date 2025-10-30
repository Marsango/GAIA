from django.contrib import admin
from .models import Propriedade, Laudo

class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'localizacao', 'proprietario', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('nome', 'localizacao', 'proprietario__first_name')
    list_editable = ('ativo',)

class LaudoAdmin(admin.ModelAdmin):
    list_display = ('numero_amostra', 'data_coleta', 'propriedade', 'ativo', 'data_criacao')
    list_filter = ('ativo', 'data_coleta', 'data_criacao')
    search_fields = ('numero_amostra', 'propriedade__nome')
    list_editable = ('ativo',)

# Registrar os models
admin.site.register(Propriedade, PropriedadeAdmin)
admin.site.register(Laudo, LaudoAdmin)