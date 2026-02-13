# 📊 DIAGRAMA VISUAL DO FLUXO DE EDIÇÃO DO CPF

## Diagrama Mermaid - Fluxo Completo

```mermaid
sequenceDiagram
    participant GUI as 👤 Interface<br/>RegisterPerson.py
    participant DBWrapper as 🌐 DatabaseHTTPWrapper<br/>edit_person()
    participant DjangoAPI as 🚀 Django API<br/>PersonViewSet
    participant Serializer as 📋 PersonSerializer<br/>update()
    participant DB[(🗄️ PostgreSQL<br/>report_person)]

    GUI->>GUI: Usuário clica "Salvar"<br/>CPF: "123.456.789-10"
    
    GUI->>DBWrapper: edit_person(person, address, id)
    
    Note over DBWrapper: 1️⃣ Normalizar CPF<br/>"123.456.789-10" → "12345678910"
    
    DBWrapper->>DB: GET /api/pessoas/{id}/
    Note over DB: Busca dados atuais
    DB-->>DBWrapper: {cpf: "12345678900", ...}
    
    Note over DBWrapper: 2️⃣ Montar payload<br/>{cpf: "12345678910", ...}
    
    DBWrapper->>DjangoAPI: PATCH /api/pessoas/{id}/<br/>{cpf: "12345678910", ...}
    
    DjangoAPI->>Serializer: validate_cpf()<br/>"12345678910"
    
    Note over Serializer: 3️⃣ Validar unicidade<br/>exclude(id=126) ✅
    
    Serializer->>Serializer: setattr(instance, 'cpf', '12345678910')
    
    Note over Serializer: 4️⃣ SALVAR NO BANCO 🔴<br/>instance.save()
    
    Serializer->>DB: UPDATE person SET<br/>cpf='12345678910'<br/>WHERE id=126
    
    Note over DB: SQL COMMIT
    DB-->>DB: CPF atualizado ✅
    
    DB-->>Serializer: OK
    
    Serializer->>Serializer: instance.refresh_from_db()<br/>Carrega do banco para confirmar
    Serializer->>DB: SELECT * FROM person WHERE id=126
    DB-->>Serializer: {cpf: "12345678910", ...}
    
    Serializer-->>DjangoAPI: Retorna Person atualizada
    DjangoAPI-->>DBWrapper: {cpf: "12345678910", ...}
    
    Note over DBWrapper: 5️⃣ Validação de Persistência<br/>GET para confirmar
    
    DBWrapper->>DB: GET /api/pessoas/{id}/
    DB-->>DBWrapper: {cpf: "12345678910", ...}
    
    Note over DBWrapper: ✅ ANTES: "12345678900"<br/>✅ DEPOIS: "12345678910"<br/>MUDANÇA CONFIRMADA!
    
    DBWrapper-->>GUI: True (sucesso)
    
    GUI->>GUI: Mostrar mensagem<br/>"✅ CPF editado com sucesso!"
```

---

## Fluxo Por Arquivo

### 1. RegisterPerson.py (Interface)

```
on_person_double_click()
   │
   ├─ person = Person(cpf="123.456.789-10")  ← COM FORMATAÇÃO
   │
   ├─ address = Address(...)
   │
   ├─ db = Database()
   │
   └─→ db.edit_person(person, address, id, requester_id)
            │
            └─→ Database.py
```

### 2. Database.py (Wrapper)

```
def edit_person(person, address, id, requester_id):
   │
   └─→ self.db.edit_person(...)
            │
            └─→ DatabaseHTTPWrapper.py
```

### 3. DatabaseHTTPWrapper.py (Núcleo da lógica)

```
def edit_person(person, address, id, requester_id):
   │
   ├─ person_dict = to_dict(person)
   │  📋 person_dict: {cpf: "123.456.789-10", ...}
   │
   ├─ current = GET /api/pessoas/{id}/
   │  📊 Dados atuais: {cpf: "12345678900", ...}
   │
   ├─ cpf_normalized = _normalize_cpf("123.456.789-10")
   │  ✅ CPF - Original: "123.456.789-10" → Normalizado: "12345678910"
   │
   ├─ birth_date_formatted = _format_date(...)
   │  ✅ Data - Original: "15/05/1990" → Formatada: "1990-05-15"
   │
   ├─ pessoa_payload = {cpf: "12345678910", ...}
   │  👤 Payload final: {cpf: "12345678910", ...}
   │
   ├─ 🔄 ENVIAR PATCH /api/pessoas/{id}/ com payload
   │  │
   │  └─→ Django API (PersonViewSet)
   │        │
   │        └─→ PersonSerializer.update()
   │            │
   │            ├─ validate_cpf() ✅
   │            │
   │            ├─ setattr(instance, 'cpf', '12345678910')
   │            │
   │            ├─ instance.save()  🔴 CRÍTICO - PERSISTE NO BANCO
   │            │
   │            └─ instance.refresh_from_db()
   │
   ├─ result = resposta do PATCH
   │
   ├─ updated = GET /api/pessoas/{id}/ (VALIDAÇÃO)
   │  📊 Dados após edição: {cpf: "12345678910", ...}
   │
   ├─ Comparar ANTES vs DEPOIS
   │  🔎 ✅ cpf: "12345678900" → "12345678910"
   │
   └─ return True/False
```

### 4. Django API (views.py)

```
PATCH /api/pessoas/126/
{cpf: "12345678910", ...}
   │
   ├─ ModelViewSet.update() (automático)
   │  │
   │  └─ PersonSerializer(instance=person, data=payload)
   │      │
   │      └─→ serializers.py
```

### 5. PersonSerializer.py

```
def update(instance, validated_data):
   │
   ├─ 🔵 PersonSerializer.update() CHAMADO
   │
   ├─ validated_data = {'cpf': '12345678910', ...}
   │
   ├─ setattr(instance, 'cpf', '12345678910')
   │  ✏️ Atualizando cpf: 12345678900 → 12345678910
   │
   ├─ 💾 instance.save()  ← AQUI PERSISTE NO BANCO!
   │
   ├─ instance.refresh_from_db()  ← AQUI RELÊ DO BANCO
   │  ✅ Pós-save: cpf = 12345678910
   │
   └─ return instance
```

### 6. PostgreSQL

```
instance.save() executa:

UPDATE report_person
SET cpf='12345678910', 
    name='João Silva',
    email='joao@example.com',
    phone_number='11987654321',
    nascimento='1990-05-15'
WHERE id=126;

✅ CPF PERSISTIDO NO BANCO!
```

---

## Pontos Críticos (🔴)

| # | Ponto | Arquivo | Função | O que pode dar erro? |
|---|-------|---------|--------|-------------------|
| 1 | CPF com formatação | RegisterPerson.py | `on_person_double_click()` | Se CPF = None/vazio, após normalização fica vazio |
| 2 | Normalização de CPF | DatabaseHTTPWrapper.py | `_normalize_cpf()` | Se entrada não tem 11+ dígitos, resultado não é 11 dígitos |
| 3 | Montagem do payload | DatabaseHTTPWrapper.py | `edit_person()` | Se payload_cpf != normalizado (buggy copy-paste) |
| 4 | PATCH request | DatabaseHTTPWrapper.py | `_make_request()` | Se retorna 400/500, API rejeita |
| 5 | Validação de CPF | PersonSerializer.py | `validate_cpf()` | Se outro Person tem este CPF, erro 400 |
| 6 | **instance.save()** | PersonSerializer.py | `update()` | **SE AQUI NÃO SALVAR, CPF NÃO PERSISTE** 🔴 |
| 7 | **refresh_from_db()** | PersonSerializer.py | `update()` | Se não recarregar, pode retornar dado em cache |
| 8 | Resposta do GET | DatabaseHTTPWrapper.py | validação | Se GET não retorna CPF novo, check ponto #6 |

---

## Estados Possíveis Após PATCH

### ✅ Estado 1: Sucesso Total
```
ANTES:  cpf = 12345678900
ENVIADO: cpf = 12345678910
DEPOIS: cpf = 12345678910

Resultado: ✅ Alteração confirmada
```

### ❌ Estado 2: Falha - CPF não mudou
```
ANTES:  cpf = 12345678900
ENVIADO: cpf = 12345678910
DEPOIS: cpf = 12345678900  ← NÃO MUDOU!

Resultado: ❌ instance.save() provavelmente não foi chamado
           ou não fez commit
```

### ❌ Estado 3: Falha - API retorna erro
```
PATCH return: None/vazio
Status: 400 Bad Request

Possíveis erros:
- CPF já cadastrado em outra pessoa
- Campo obrigatório vazio
- Formato inválido
```

### ⚠️ Estado 4: Sucesso relativo - GUI não atualiza
```
Banco: cpf = 12345678910 (correto)
GUI: cpf = 12345678900 (antigo)

Resultado: ⚠️ CPF foi salvo, mas GUI não recarregou os dados
```

---

## Teste Rápido - Verificar Cada Ponto

```python
# 1. Verificar if CPF está sendo normalizado
print(DatabaseHTTPWrapper()._normalize_cpf("123.456.789-10"))
# Output: "12345678910"  ✅

# 2. Verificar if PersonSerializer.update() salva
from report.models import Person
from report.serializers import PersonSerializer

pessoa = Person.objects.get(id=126)
s = PersonSerializer(pessoa, data={'cpf': '99999999999'}, partial=True)
if s.is_valid():
    s.save()
    pessoa.refresh_from_db()
    print(pessoa.cpf)  # Deve ser '99999999999'

# 3. Verificar if API retorna dados atualizados
# Via curl ou insomnia:
PATCH http://localhost:8000/api/pessoas/126/
{cpf: "99999999999"}
# Response deve ter cpf: "99999999999"

# 4. Verificar if banco foi realmente alterado
SELECT cpf FROM report_person WHERE id=126;
# Deve retornar '99999999999'
```

---

## Resumo: Onde CPF pode se perder

```
(1) Input da GUI
    ↓
(2) Normalização em DatabaseHTTPWrapper
    ↓
(3) Payload montado corretamente
    ↓
(4) PATCH enviado para API
    ↓
(5) Validação em PersonSerializer.validate_cpf()  ← Pode rejeitar
    ↓
(6) Instance.save() em PersonSerializer.update()  ← 🔴 CRÍTICO: Se não salvar aqui
    ↓
(7) Dados retornam da API
    ↓
(8) Validação de persistência em DatabaseHTTPWrapper  ← Detecta falha em (6)
```

Se CPF não está sendo persistido no banco, o problema está em **ponto (6)**.
