# 🔍 Análise Completa do Fluxo de Edição do CPF

## 📋 Resumo Executivo

A edição do CPF segue este fluxo:
```
Interface GUI (RegisterPerson.py)
    ↓ Usuário clica "Salvar"
    ↓
Cria objeto Person com novo CPF
    ↓
Chama db.edit_person(person, address, id, requester_id)
    ↓
Database.py Wrapper
    ↓ Delega para DatabaseHTTPWrapper
    ↓
DatabaseHTTPWrapper.edit_person()
    ↓ Normaliza CPF (remove caracteres, deixa 11 dígitos)
    ↓ Formata data (DD/MM/YYYY → YYYY-MM-DD)
    ↓
Envia PATCH /api/pessoas/{id}/ com payload normalizado
    ↓
Django API - PersonViewSet
    ↓ Recebe PATCH, chama serializer.update()
    ↓
PersonSerializer.update()
    ↓ validate_cpf() - Verifica unicidade
    ↓ setattr(instance, 'cpf', cpf_normalizado)
    ↓ instance.save() - **PERSISTE NO BANCO**
    ↓ instance.refresh_from_db() - **CONFIRMA PERSISTÊNCIA**
    ↓
PostgreSQL Database
    ↓ UPDATE person SET cpf='...' WHERE id=X
    ↓
Retorna dados atualizados
    ↓
DatabaseHTTPWrapper valida persistência com GET /api/pessoas/{id}/
    ↓
Compara ANTES vs DEPOIS
    ↓
Interface mostra "CPF editado com sucesso"
```

---

## 🔧 1. INTERFACE (RegisterPerson.py)

### Local: `interface/RegisterPerson.py` - Linhas 235-255

```python
def on_person_double_click(self):
    """Quando usuário clica em Salvar após editar dados"""
    # ... validação de campos ...
    
    person = Person(
        name=self.name_line.text(),
        cpf=self.cpf_line.text(),  # ← CPF como recebido da GUI (pode estar formatado)
        email=self.email_line.text(),
        phone_number=self.phone_line.text(),
        birth_date=data_nascimento
    )
    
    address = Address(
        street=self.street_line.text(),
        address_number=self.address_num_line.text(),
        city=self.city_line.text(),
        state=self.state_line.text(),
        country=self.country_line.text(),
        cep=self.cep_line.text()
    )
    
    # ← AQUI: CPF pode estar como "123.456.789-10" (COM FORMATAÇÃO)
    db = Database()
    result = db.edit_person(person, address, self.current_person_id, self.requester_id)
    
    if result:
        self.show_message("✅ Pessoa editada com sucesso!")
    else:
        self.show_message("❌ Erro ao editar pessoa")
```

**Observação Crítica**: O CPF chega da GUI potencialmente FORMATADO (ex: "123.456.789-10")

---

## 🗄️ 2. WRAPPER DATABASE (Database.py)

### Local: `backend/classes/Database.py`

```python
def edit_person(self, person: Person, address: Address, id: int, requester_id: int) -> bool:
    """Wrapper que delega para DatabaseHTTPWrapper"""
    return self.db.edit_person(person, address, id, requester_id)
```

**Função**: Apenas delega para `self.db` (que é uma instância de `DatabaseHTTPWrapper`)

---

## 🌐 3. CAMADA HTTP (DatabaseHTTPWrapper.py)

### Local: `backend/classes/DatabaseHTTPWrapper.py` - Linhas 410-537

#### 3.1 Entrada
```python
def edit_person(self, person: Person, address: Address, id: int, requester_id: int):
    """Edita Person via PATCH para Django API"""
```

#### 3.2 Conversão para Dicionário (Linhas 414-415)
```python
person_dict = to_dict(person)
address_dict = to_dict(address)

print(f"📋 person_dict: {person_dict}", flush=True)
print(f"📋 address_dict: {address_dict}", flush=True)
```

**Output no console**:
```
📋 person_dict: {'name': 'João Silva', 'cpf': '123.456.789-10', 'email': '...', ...}
```

#### 3.3 Fetch Dados Atuais (Linhas 419-423)
```python
current = self._make_request("GET", f"/api/pessoas/{id}/") or {}
```

**Exemplo de `current`**:
```python
{
    "id": 126,
    "name": "João Silva",
    "cpf": "12345678910",  # ← Banco tem CPF NORMALIZADO (11 dígitos)
    "email": "joao@example.com",
    "phone_number": "11987654321",
    "nascimento": "1990-05-15"
}
```

#### 3.4 📌 NORMALIZAÇÃO DO CPF (Linhas 450-452) - CRÍTICO

```python
cpf_raw = person_dict.get("cpf", current.get("cpf", ""))
# pessoa_dict.get("cpf") = "123.456.789-10" (COM FORMATAÇÃO)

cpf_normalized = self._normalize_cpf(cpf_raw)
# ↓ Chama método _normalize_cpf (Linhas 98-102)

def _normalize_cpf(self, cpf: str) -> str:
    """Remove formatação do CPF, deixando apenas 11 dígitos"""
    if not cpf:
        return ""
    return ''.join(filter(str.isdigit, str(cpf)))
    # "123.456.789-10" → "12345678910" ✅

print(f"🆔 CPF - Original: '{cpf_raw}' → Normalizado: '{cpf_normalized}'", flush=True)
```

**Console Output**:
```
🆔 CPF - Original: '123.456.789-10' → Normalizado: '12345678910'
```

#### 3.5 Formatação da Data (Linhas 454-456)
```python
birth_date_raw = person_dict.get("birth_date") or current.get("nascimento")
birth_date_formatted = self._format_date(birth_date_raw)
print(f"📅 Data - Original: '{birth_date_raw}' → Formatada: '{birth_date_formatted}'", flush=True)
```

**Exemplo**:
```
📅 Data - Original: '15/05/1990' → Formatada: '1990-05-15'
```

#### 3.6 Montagem do Payload (Linhas 460-474)
```python
pessoa_payload = {
    "name": person_dict.get("name", current.get("name", "")),
    "cpf": cpf_normalized,  # ← CPF NORMALIZADO (11 dígitos)
    "email": person_dict.get("email", current.get("email", "")),
    "phone_number": phone or current.get("phone_number", ""),
    "nascimento": birth_date_formatted,  # ← Data formatada (YYYY-MM-DD)
}

print(f"👤 Payload final da pessoa: {pessoa_payload}", flush=True)
```

**Console Output**:
```
👤 Payload final da pessoa: {
    'name': 'João Silva',
    'cpf': '12345678910',
    'email': 'joao@example.com',
    'phone_number': '11987654321',
    'nascimento': '1990-05-15'
}
```

#### 3.7 Comparação ANTES vs DEPOIS (Linhas 475-477)
```python
print(f"🔄 Comparação ANTES vs DEPOIS:")
print(f"   cpf: '{current.get('cpf')}' → '{pessoa_payload['cpf']}'")
```

**Exemplo**:
```
🔄 Comparação ANTES vs DEPOIS:
   cpf: '12345678900' → '12345678910'
```

#### 3.8 🔴 ENVIO DO PATCH (Linhas 487-488) - **PONTO CRÍTICO**
```python
print(f"🔄 Enviando PATCH para /api/pessoas/{id}/", flush=True)
result = self._make_request("PATCH", f"/api/pessoas/{id}/", data=pessoa_payload)
```

**O que é enviado**:
```
PATCH /api/pessoas/126/
Content-Type: application/json

{
    "name": "João Silva",
    "cpf": "12345678910",
    "email": "joao@example.com",
    "phone_number": "11987654321",
    "nascimento": "1990-05-15"
}
```

#### 3.9 Validação de Persistência (Linhas 491-537)
```python
if result:
    print(f"✅ Pessoa editada com sucesso! Resultado: {result}", flush=True)
    
    # VALIDAÇÃO CRÍTICA: Verificar se mudança realmente persistiu
    updated = self._make_request("GET", f"/api/pessoas/{id}/")
    print(f"📊 Dados após edição: {updated}", flush=True)
    
    # Comparar cada campo crítico
    campos_criticos = ['name', 'cpf', 'email', 'phone_number', 'nascimento']
    
    mudancas_confirmadas = []
    mudancas_nao_confirmadas = []
    
    for campo in campos_criticos:
        valor_antes = current.get(campo)
        valor_depois = updated.get(campo)
        valor_solicitado = pessoa_payload.get(campo)
        
        if valor_antes != valor_depois:
            mudancas_confirmadas.append(f"✅ {campo}: '{valor_antes}' → '{valor_depois}'")
        elif valor_solicitado and valor_antes == valor_depois and valor_solicitado != valor_antes:
            mudancas_nao_confirmadas.append(f"❌ {campo}: solicitado '{valor_solicitado}' mas permanece '{valor_depois}'")
```

**Console Output - Caso de Sucesso**:
```
✅ Pessoa editada com sucesso! Resultado: {...}
📊 Dados após edição: {...}

🔎 VALIDAÇÃO DE PERSISTÊNCIA:
   ✅ cpf: '12345678900' → '12345678910'
   ✅ name: 'João Silva' → 'João Silva'
   ✅ email: 'joao@example.com' → 'joao@example.com'
```

**Console Output - Caso de Falha** (⚠️ ALERTA):
```
✅ Pessoa editada com sucesso!
📊 Dados após edição: {cpf: '12345678900', ...}  ← CPF NÃO MUDOU!

🔎 VALIDAÇÃO DE PERSISTÊNCIA:
   ❌ cpf: solicitado '12345678910' mas permanece '12345678900'
   
⚠️ ALERTA: Algumas mudanças NÃO foram persistidas no backend!
   Isso indica um problema na API Django (serializer não está salvando)
   Tentando com PUT completo como fallback...
```

---

## 🚀 4. DJANGO API (views.py & serializers.py)

### 4.1 Request chega em PersonViewSet

**Arquivo**: `Web/gaia_backend/report/views.py` - Linhas 15-100

PersonViewSet é um `ModelViewSet`, então ao receber PATCH `/api/pessoas/126/`:
1. O DRF (Django REST Framework) chama automaticamente o método `update()`
2. Que por sua vez trata a requisição PATCH
3. Instancia o `PersonSerializer` com os dados
4. Chama `serializer.update(instance, validated_data)`

```python
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
```

### 4.2 PersonSerializer - Validação de CPF (Linhas 140-156)

**Arquivo**: `Web/gaia_backend/report/serializers.py`

```python
def validate_cpf(self, value):
    """Valida CPF único no modelo Person (report)"""
    
    # Remover formatação (normalizando)
    cpf_limpo = ''.join(filter(str.isdigit, str(value)))
    # '12345678910' → '12345678910' (já normalizado, nada muda)
    
    instance = self.instance  # É a Person que está sendo atualizada
    if instance:
        # Atualização - verificar se mudou
        if Person.objects.filter(cpf=cpf_limpo).exclude(id=instance.id).exists():
            # ⚠️ Se OUTRO registro tiver este CPF, error!
            raise serializers.ValidationError(
                f'CPF {value} já está cadastrado para outra pessoa.'
            )
    else:
        # Criação (não é este caso)
        if Person.objects.filter(cpf=cpf_limpo).exists():
            raise serializers.ValidationError(
                f'CPF {value} já está cadastrado.'
            )
    
    return cpf_limpo  # Retorna CPF normalizado
```

**Fluxo**:
1. ✅ DRF passa `cpf='12345678910'`
2. ✅ validate_cpf() é chamado
3. ✅ Valida que nenhuma OUTRA pessoa tem este CPF
4. ✅ Retorna CPF normalizado: `'12345678910'`

**⚠️ Possível Problema**: Se o usuário está mudando de CPF para um que já existe, vai dar erro aqui.

### 4.3 PersonSerializer.update() - SALVA NO BANCO (Linhas 174-193)

```python
def update(self, instance, validated_data):
    """
    Método explícito para UPDATE - FORÇA a persistência dos dados
    """
    print(f"\n🔵 PersonSerializer.update() CHAMADO", flush=True)
    print(f"   Instance ID: {instance.id}", flush=True)
    print(f"   Validated data: {validated_data}", flush=True)
    # Exemplo output:
    # Instance ID: 126
    # Validated data: {'cpf': '12345678910', 'name': 'João Silva', ...}
    
    # Atualizar cada campo
    for attr, value in validated_data.items():
        print(f"   Atualizando {attr}: {getattr(instance, attr, 'N/A')} → {value}", flush=True)
        # Exemplo output:
        # Atualizando cpf: 12345678900 → 12345678910
        setattr(instance, attr, value)
    
    # 🔴 SALVAR EXPLICITAMENTE - CRÍTICO
    print(f"   💾 Salvando no banco de dados...", flush=True)
    instance.save()  
    # ← Aqui é que o CPF é persistido no PostgreSQL!
    
    # Verificar que foi salvo
    instance.refresh_from_db()  # Força reload do banco
    print(f"   ✅ Salvo! Verificação pós-save:", flush=True)
    for attr in validated_data.keys():
        print(f"      {attr}: {getattr(instance, attr)}", flush=True)
    # Exemplo output:
    #    cpf: 12345678910  ← CONFIRMADO que salvou!
    
    return instance  # Retorna a Person atualizada
```

**Console Output - Sucesso**:
```
🔵 PersonSerializer.update() CHAMADO
   Instance ID: 126
   Validated data: {'cpf': '12345678910', 'name': 'João Silva', ...}
   Atualizando cpf: 12345678900 → 12345678910
   Atualizando name: João Silva → João Silva
   💾 Salvando no banco de dados...
   ✅ Salvo! Verificação pós-save:
      cpf: 12345678910
      name: João Silva
```

---

## 🗄️ 5. POSTGRESQL DATABASE

Quando `instance.save()` é executado, Django:
1. Gera SQL: `UPDATE person SET cpf='12345678910' WHERE id=126`
2. Envia para PostgreSQL
3. PostgreSQL atualiza o registro
4. Retorna sucesso

**SQL Executado**:
```sql
UPDATE report_person 
SET cpf='12345678910', name='João Silva', email='joao@example.com', 
    phone_number='11987654321', nascimento='1990-05-15'
WHERE id=126;
```

---

## 🔴 POSSÍVEIS PROBLEMAS E SOLUÇÕES

### Problema 1: CPF não persiste (API retorna sucesso mas BD não atualiza)

**Sintomas**:
- Console mostra: `✅ Pessoa editada com sucesso!`
- Mas a validação de persistência mostra: `❌ cpf: solicitado '12345678910' mas permanece '12345678900'`
- O código tenta PUT como fallback

**Possíveis Causas**:

#### A. Serializer.update() não está sendo chamado
**Diagnóstico**: Verificar se há overrides do método `update()` em algum lugar que não chamam `instance.save()`
**Solução**: PersonSerializer.update() já tem `instance.save()` explícito

#### B. Constraint de Unicidade bloqueando UPDATE
**Diagnóstico**: Django teria gerado erro 400 com mensagem sobre duplicate CPF
**Solução**: Validador já trata com `exclude(id=instance.id)`

#### C. Transação não sendo commitada
**Diagnóstico**: Verificar logs de erro 500 no Django
**Solução**: Django auto-commita após requisição HTTP bem-sucedida

#### D. A API está retornando dados na memória , não do banco
**Diagnóstico**: Serializer retorna `instance` logo após `save()`, que ainda tem dados em memória
**Solução**: Já fazemos `instance.refresh_from_db()` para forçar reload do BD

#### E. Múltiplos registros com mesmo CPF
**Diagnóstico**: Existem 2+ registros de Person com CPF '12345678900'
**Solução**: Executar query SQL para identificar duplicatas

### Problema 2: API retorna erro 400 (Bad Request)

**Sintomas**: `_make_request()` retorna None, edit falha

**Possíveis Causas**:
- CPF violando constraint de unicidade
- Email violando constraint de unicidade
- Data em formato inválido
- Campos obrigatórios não foram enviados

**Solução**: Verificar resposta de erro com field-by-field

---

## 🧪 TESTE PRÁTICO

### Teste 1: Verificar se o fluxo inteiro está funcionando
```
1. Abra interface/RegisterPerson.py
2. Edite uma pessoa mudando o CPF (ex: de 12345678900 para 12345678910)
3. Clique em Salvar
4. Verifique a saída do console do servidor Django:
   - Procure por "🔄 Enviando PATCH"
   - Procure por "🔵 PersonSerializer.update() CHAMADO"
   - Procure por "💾 Salvando no banco de dados..."
   - Procure por "✅ Salvo!"
5. Na sequência, procure por "📊 Dados após edição" na saída de DatabaseHTTPWrapper
6. Verifique a linha "🔎 VALIDAÇÃO DE PERSISTÊNCIA" - todos os campos devem ter ✅
```

### Teste 2: Verificar banco de dados diretamente
```sql
-- No terminal PostgreSQL:
psql -U seu_user -d sua_database

SELECT id, cpf, name FROM report_person WHERE id=126;

-- Verifique se CPF é realmente '12345678910'
```

### Teste 3: Forçar erro para diagnóstico
```
1. Crie uma segunda pessoa com CPF '99999999910'
2. Tente editar a pessoa ID 126 com CPF '99999999910'
3. Deverá dar erro 400 (duplicate CPF)
4. Verifique a mensagem de erro no console
```

---

## 📊 DIAGRAMA DO FLUXO

```
┌─────────────────────────────┐
│  RegisterPerson.py (GUI)    │
│ Usuário edita CPF           │
│ CPF: "123.456.789-10"       │ ← FORMATADO
└────────────┬────────────────┘
             │
             ↓
┌─────────────────────────────┐
│  Database.py (Wrapper)      │
│ db.edit_person()            │
└────────────┬────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│  DatabaseHTTPWrapper.py                 │
│  edit_person()                          │
└────────────┬────────────────────────────┘
             │
             ├─→ to_dict(person)          → cpf="123.456.789-10"
             │
             ├─→ GET /api/pessoas/126/   → current CPF="12345678900"
             │
             ├─→ _normalize_cpf()        → "12345678910" ✅
             │
             ├─→ _format_date()          → "1990-05-15" ✅
             │
             └─→ pessoa_payload          → cpf="12345678910"
                      │
                      ↓
                ┌─────────────────────────────────────────┐
                │ PATCH /api/pessoas/126/                 │
                │ {cpf: "12345678910", ...}              │
                └────────────┬────────────────────────────┘
                             │
                             ↓
        ┌────────────────────────────────────────────────┐
        │  Django API - PersonViewSet                    │
        │  ModelViewSet recebe PATCH                     │
        └────────────┬─────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────────────┐
        │  PersonSerializer.update()                     │
        │  - validate_cpf()  → "12345678910" ✅         │
        │  - setattr() CPF                               │
        │  - instance.save() → **PERSISTE** 🔴           │
        │  - refresh_from_db() → Carrega do BD           │
        └────────────┬─────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────────────┐
        │  PostgreSQL                                    │
        │  UPDATE person SET cpf='12345678910'          │
        │  WHERE id=126                                  │
        └────────────┬─────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────────────┐
        │  Retorna Person com novo CPF                   │
        └────────────┬─────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────┐
│  DatabaseHTTPWrapper                    │
│  GET /api/pessoas/126/ (validação)     │
│  Compara ANTES vs DEPOIS                │
│  ✅ = sucesso                           │
│  ❌ = falha (tenta PUT fallback)        │
└─────────────────────────────────────────┘
```

---

## 📝 RESUMO DOS PONTOS CRÍTICOS

| Ponto | Arquivo | Função | Ação Crítica |
|-------|---------|--------|-------------|
| 1 | RegisterPerson.py | `on_person_double_click()` | CPF pode estar formatado |
| 2 | DatabaseHTTPWrapper.py | `_normalize_cpf()` | Remove formatação → 11 dígitos |
| 3 | DatabaseHTTPWrapper.py | `edit_person()` | Monta payload com CPF normalizado |
| 4 | DatabaseHTTPWrapper.py | `_make_request()` | Envia PATCH com payload |
| 5 | PersonViewSet.py | update() (implícito) | Instancia serializer |
| 6 | PersonSerializer.py | `validate_cpf()` | Valida unicidade (exclude self) |
| 7 | PersonSerializer.py | `update()` | **instance.save()** ← **PERSISTE** |
| 8 | PostgreSQL | UPDATE | Executa SQL no banco |
| 9 | DatabaseHTTPWrapper.py | validação de persistência | GET para confirmar |

---

## 🎯 PRÓXIMOS PASSOS

1. **Executar testes práticos acima** para diagnosticar exatamente onde o problema está
2. **Verificar logs do Django** durante a operação de PATCH
3. **Verificar banco de dados** com SQL direto para ver se CPF realmente não está sendo atualizado
4. Se CPF não está sendo salvo no banco, o problema é em PersonSerializer.update() ou no PostgreSQL
5. Se CPF está sendo salvo mas não é mostrado na GUI, o problema é no refresh de dados
