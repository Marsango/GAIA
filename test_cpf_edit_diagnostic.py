#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE DE DIAGNÓSTICO - Edição de CPF

Este script ajuda a diagnosticar exatamente onde o CPF não está sendo persistido.

COMO USAR:
1. Execute este script no terminal da GUI
2. Ele va aperguntar qual person_id testar
3. Vai mostrar o CPF atual no banco
4. Vai simular os passos da edição
5. Va informar exatamente onde o problema está
"""

import sys
import os

# Adicionar o backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from classes.Database import Database
from classes.Person import Person
from classes.Address import Address


def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_cpf_edit():
    """Teste completo de edição de CPF"""
    
    print_section("🧪 TESTE DE DIAGNÓSTICO - EDIÇÃO DE CPF")
    
    # 1. INPUT DO USUÁRIO
    print("Digite o ID da pessoa que deseja testar (ex: 126):")
    try:
        person_id = int(input("> ").strip())
    except:
        print("❌ ID inválido!")
        return
    
    print(f"\n✓ Testando edição da pessoa ID {person_id}")
    
    # 2. CONECTAR AO BANCO
    print_section("PASSO 1: Conectando ao banco de dados")
    try:
        db = Database()
        print("✅ Conexão estabelecida com DatabaseHTTPWrapper")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # 3. BUSCAR PESSOA ATUAL
    print_section("PASSO 2: Buscando dados atuais da pessoa")
    print(f"Enviando GET /api/pessoas/{person_id}/")
    
    # Simulamos uma requisição GET
    from backend.classes.DatabaseHTTPWrapper import DatabaseHTTPWrapper
    wrapper = db.db  # DatabaseHTTPWrapper instance
    
    try:
        current = wrapper._make_request("GET", f"/api/pessoas/{person_id}/")
        if not current:
            print(f"❌ Pessoa ID {person_id} não encontrada!")
            return
        
        print(f"\n✅ Dados atuais recebidos:")
        print(f"   ID: {current.get('id')}")
        print(f"   Nome: {current.get('name')}")
        print(f"   CPF ATUAL (no banco): '{current.get('cpf')}'")
        print(f"   Email: {current.get('email')}")
        print(f"   Telefone: {current.get('phone_number')}")
        print(f"   Data de Nascimento: {current.get('nascimento')}")
        
        cpf_atual = current.get('cpf', '')
        
    except Exception as e:
        print(f"❌ Erro ao buscar pessoa: {e}")
        return
    
    # 4. PEDIR NOVO CPF
    print_section("PASSO 3: Solicitar novo CPF para editar")
    print(f"CPF atual no banco: {cpf_atual}")
    print("Digite o novo CPF (com ou sem formatação):")
    cpf_novo = input("> ").strip()
    
    if not cpf_novo:
        print("❌ CPF vazio!")
        return
    
    # 5. SIMULAR NORMALIZAÇÃO
    print_section("PASSO 4: Normalizar CPF (remover formatação)")
    cpf_normalized = ''.join(filter(str.isdigit, cpf_novo))
    print(f"CPF Original: '{cpf_novo}'")
    print(f"CPF Normalizado: '{cpf_normalized}'")
    
    if len(cpf_normalized) != 11:
        print(f"⚠️  AVISO: CPF normalizado tem {len(cpf_normalized)} dígitos, esperado 11")
    else:
        print(f"✅ CPF normalizado corretamente (11 dígitos)")
    
    # 6. MONTAR PAYLOAD
    print_section("PASSO 5: Montar payload para PATCH")
    payload = {
        "name": current.get('name'),
        "cpf": cpf_normalized,
        "email": current.get('email'),
        "phone_number": current.get('phone_number'),
        "nascimento": current.get('nascimento')
    }
    
    print("Payload que será enviado:")
    for key, value in payload.items():
        print(f"   {key}: {value}")
    
    # 7. ENVIAR PATCH
    print_section("PASSO 6: Enviar PATCH para Django API")
    print(f"Enviando: PATCH /api/pessoas/{person_id}/ com payload acima")
    
    try:
        result = wrapper._make_request("PATCH", f"/api/pessoas/{person_id}/", data=payload)
        if result:
            print(f"✅ API retornou sucesso!")
            print(f"   Resposta: {result.get('cpf')}")
        else:
            print(f"❌ API retornou vazio (None)")
            return
    except Exception as e:
        print(f"❌ Erro ao fazer PATCH: {e}")
        return
    
    # 8. VALIDAR PERSISTÊNCIA
    print_section("PASSO 7: Validar se CPF foi persistido (GET para confirmar)")
    print(f"Enviando: GET /api/pessoas/{person_id}/ para verificar")
    
    try:
        updated = wrapper._make_request("GET", f"/api/pessoas/{person_id}/")
        if not updated:
            print(f"❌ Não conseguiu buscar pessoa após PUT")
            return
        
        cpf_apos = updated.get('cpf')
        print(f"\n✅ Dados após edição:")
        print(f"   CPF (no banco): '{cpf_apos}'")
        
    except Exception as e:
        print(f"❌ Erro ao validar: {e}")
        return
    
    # 9. DIAGNÓSTICO FINAL
    print_section("🔍 DIAGNÓSTICO FINAL")
    
    print(f"CPF ANTES: '{cpf_atual}'")
    print(f"CPF SOLICITADO: '{cpf_normalized}'")
    print(f"CPF DEPOIS: '{cpf_apos}'")
    
    if cpf_apos == cpf_normalized:
        print(f"\n✅ ✅ ✅ SUCESSO! CPF foi atualizado corretamente!")
        print(f"\nO problema deve estar:")
        print(f"   - Na GUI (não recarrega dados após edição)")
        print(f"   - OU no fluxo de criação da Person object")
    
    elif cpf_apos == cpf_atual:
        print(f"\n❌ ❌ ❌ CPF NÃO FOI ALTERADO!")
        print(f"\nO problema está em um destes pontos:")
        print(f"   1. PersonSerializer.update() não é chamado")
        print(f"   2. instance.save() não está salvando no banco")
        print(f"   3. Constraint de unicidade está bloqueando")
        print(f"   4. Transação não está sendo commitada")
        print(f"\n🔧 PRÓXIMOS PASSOS:")
        print(f"   - Verificar logs do Django durante PATCH")
        print(f"   - Verificar se há erro 400 em resposta de erro")
        print(f"   - Executar SQL: SELECT * FROM report_person WHERE id={person_id}")
    
    else:
        print(f"\n⚠️  CPF MUDOU PARA ALGO INESPERADO!")
        print(f"   Mudou para: '{cpf_apos}'")
        print(f"   Esperado: '{cpf_normalized}'")
        print(f"   Isso sugere um problema de validação ou normalização")
    
    print_section("✅ TESTE CONCLUÍDO")


def test_direct_serializer():
    """Teste direto no serializer (Django shell)"""
    print_section("🧪 TESTE DIRETO NO SERIALIZER")
    
    print("""
Para testar diretamente se PersonSerializer.update() está funcionando:

1. Na pasta Web/gaia_backend, execute Django shell:
   python manage.py shell

2. Cole o código abaixo:

```python
from report.models import Person
from report.serializers import PersonSerializer

# Buscar uma pessoa
pessoa = Person.objects.get(id=126)
print(f"CPF antes: {pessoa.cpf}")

# Criar serializer com dados novos
data = {
    'name': pessoa.name,
    'cpf': '99999999900',  # ← Novo CPF (diferente)
    'email': pessoa.email,
    'phone_number': pessoa.phone_number,
    'nascimento': pessoa.nascimento
}

serializer = PersonSerializer(pessoa, data=data, partial=True)
if serializer.is_valid():
    serializer.save()
    print(f"CPF depois: {pessoa.cpf}")
    
    # Verificar no banco
    pessoa.refresh_from_db()
    print(f"CPF após refresh: {pessoa.cpf}")
else:
    print(f"Erros: {serializer.errors}")
```

3. Verifique se o CPF mudou no consola
4. Se mudar, o serializer está OK
5. Se não mudar, o problema está no serializer.update() ou no modelo
    """)


if __name__ == "__main__":
    try:
        test_cpf_edit()
        # Após test_cpf_edit, oferecer teste alternativo
        print("\n\nDeseja fazer teste alternativo direto no Django shell? (s/n)")
        if input("> ").lower().startswith('s'):
            test_direct_serializer()
    except KeyboardInterrupt:
        print("\n\n❌ Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
