#!/usr/bin/env python
"""
Script para debugar o erro no Step 8 (edit amostra)
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django com SQLite temporariamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Override do banco de dados para teste
if not settings.configured:
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

django.setup()

# Criar tabelas
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

from report.models import Amostra, Propriedade, Person, Endereco
from report.serializers import AmostraSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import date

User = get_user_model()

# Criar teste
print("=== DEBUG: Testando Amostra Serializer ===\n")

# Primeiro, criar dados de teste
print("1. Criando dados de teste...")

try:
    # Criar endereço
    addr = Endereco.objects.create(
        cep="99999999",
        rua="Rua Debug",
        numero="999",
        cidade="Sao Paulo",
        estado="SP",
        pais="Brasil"
    )
    print(f"OK: Endereco criado: {addr.id}")
    
    # Criar pessoa
    person = Person.objects.create(
        name="Debug Person",
        cpf="99988877700",
        email="debug@test.com",
        phone_number="(11) 99999-8888",
        nascimento="1990-01-15",
        endereco=addr
    )
    print(f"OK: Pessoa criada: {person.id}")
    
    # Criar propriedade
    prop = Propriedade.objects.create(
        name="Debug Property",
        registration_number=999999,
        proprietario_pessoa=person,
        endereco=addr
    )
    print(f"OK: Propriedade criada: {prop.id}")
    
    # Criar amostra
    amostra = Amostra.objects.create(
        propriedade=prop,
        numero_amostra=5000,
        data_coleta=date.today(),
        ph=6.5,
        fosforo=10.5,
        potassio=150,
        materia_organica=2.5,
        argila=25,
        silte=15,
        areia=60,
        descricao="Test amostra"
    )
    print(f"OK: Amostra criada: {amostra.id}")
    
except Exception as e:
    print(f"ERRO ao criar dados: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Agora testar update
print("\n2. Testando serializacao (GET)...")
try:
    serializer = AmostraSerializer(amostra)
    print(f"OK: Dados serializados")
    print(f"Campos: {list(serializer.data.keys())}")
except Exception as e:
    print(f"ERRO ao serializar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Testar update
print("\n3. Testando atualizacao (PUT)...")
try:
    updated_data = {
        "propriedade": prop.id,
        "numero_amostra": 5001,
        "data_coleta": str(date.today()),
        "ph": 7.0,
        "fosforo": 12.0,
        "potassio": 160,
        "materia_organica": 3.0,
        "argila": 30,
        "silte": 20,
        "areia": 50,
        "descricao": "Updated test amostra"
    }
    
    serializer = AmostraSerializer(amostra, data=updated_data, partial=False)
    
    if serializer.is_valid():
        serializer.save()
        print(f"OK: Amostra atualizada com sucesso!")
    else:
        print(f"ERRO de validacao: {serializer.errors}")
        exit(1)
        
except Exception as e:
    print(f"ERRO ao atualizar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n=== DEBUG: Todos os testes passaram! ===")
