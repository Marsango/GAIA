from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Customizar a exibição do usuário no admin
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'cpf', 'first_name', 'last_name', 'email', 'telefone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'cpf', 'first_name', 'last_name', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('cpf', 'telefone')
        }),
    )

# Registrar o model Usuario
admin.site.register(Usuario, UsuarioAdmin)