# 🐛 GUIA DE DEBUG - Como usar os logs existentes

## 🎯 Objetivo

Os logs já estão implementados em todo o fluxo de edição de CPF. Esse guia mostra como ler e interpretar os logs para diagnosticar o problema.

---

## 📍 ONDE ENCONTRAR OS LOGS

### 1. Logs de DatabaseHTTPWrapper.py
**Saída**: Console da aplicação GUI (onde você rodou a interface)
**Identifica por**: Linhas começando com `🔄`, `🆔`, `📅`, `👤`, `💾`, `✅`, `❌`

### 2. Logs de PersonSerializer.py
**Saída**: Console do servidor Django (onde você rodou `python manage.py runserver`)
**Identifica por**: Linhas começando com `🔵`, `💾`, `✅`

### 3. Logs de PostgreSQL (opcional)
**Saída**: Logs do PostgreSQL (geralmente em `/var/lib/postgresql/logs/` ou `C:\Program Files\PostgreSQL\XX\data\log\`)
**Identifica por**: `UPDATE report_person SET...`

---

## 🔍 FLUXO COMPLETO COM LOGS

### TESTE: Editar CPF de 12345678900 para 12345678910

#### PASSO 1: GUI (RegisterPerson.py) - Sem log aqui
- Usuário clica "Salvar"
- RegisterPerson.py cria objeto Person

#### PASSO 2: DatabaseHTTPWrapper - Vários logs

**Console da GUI**:
```
📋 person_dict: {'name': 'João Silva', 'cpf': '123.456.789-00', ...}
📍 Buscando dados atuais de pessoa ID 126...
📊 Dados atuais: {'id': 126, 'cpf': '12345678900', 'name': 'João Silva', ...}
🆔 CPF - Original: '123.456.789-00' → Normalizado: '12345678900'
```

**⚠️ PROBLEMA DETECTADO AQUI**: Se disser `→ Normalizado: ''` (vazio), é problema de input.

```
📅 Data - Original: '15/05/1990' → Formatada: '1990-05-15'
👤 Payload final da pessoa: {'name': 'João Silva', 'cpf': '12345678910', ...}
🔄 Comparação ANTES vs DEPOIS:
   cpf: '12345678900' → '12345678910'
🔄 Enviando PATCH para /api/pessoas/126/
```

**⚠️ PROBLEMA DETECTADO AQUI**: Se não aparecer `🔄 Enviando PATCH`, é erro antes disso.

#### PASSO 3: Django API - Logs no console do Django

**Console do servidor Django** (`python manage.py runserver`):
```
🔵 PersonSerializer.update() CHAMADO
   Instance ID: 126
   Validated data: {'cpf': '12345678910', 'name': 'João Silva', ...}
   Atualizando cpf: 12345678900 → 12345678910
   Atualizando name: João Silva → João Silva
   💾 Salvando no banco de dados...
```

**⚠️ PROBLEMA DETECTADO AQUI**: Se não aparecer `🔵 PersonSerializer.update()`, o DRF não está chamando o serializer.

```
   ✅ Salvo! Verificação pós-save:
      cpf: 12345678910
      name: João Silva
```

**⚠️ PROBLEMA DETECTADO AQUI**: Se `cpf` continua `12345678900` após pós-save, é problema em `instance.save()`.

#### PASSO 4: Volta para DatabaseHTTPWrapper - Validação final

**Console da GUI**:
```
✅ Pessoa editada com sucesso! Resultado: {...}
🔍 Verificando persistência...
📊 Dados após edição: {'id': 126, 'cpf': '12345678910', ...}

🔎 VALIDAÇÃO DE PERSISTÊNCIA:
   ✅ cpf: '12345678900' → '12345678910'
   ✅ name: 'João Silva' → 'João Silva'
```

**✅ SUCESSO!** CPF foi persistido corretamente.

---

## ❌ CENÁRIOS DE FALHA E COMO IDENTIFICAR

### Cenário 1: CPF normalizado vem vazio

**Console da GUI**:
```
📋 person_dict: {'cpf': '', ...}  ← CPF vazio!
🆔 CPF - Original: '' → Normalizado: ''
```

**Diagnóstico**: Seja `None` ou string vazia em Person.cpf
**Solução**: Verificar se RegisterPerson.py está limpando o campo por engano

---

### Cenário 2: PATCH não é enviado

**Console da GUI**:
```
👤 Payload final da pessoa: {'cpf': '12345678910', ...}
❌ Falha ao editar pessoa - resultado vazio
```

**Diagnóstico**: `_make_request()` voltou None/vazio
**Solução**: Verificar resposta da API (pode ser erro 400 ou 500)

**Para diagnosticar melhor**: Adicione este código em DatabaseHTTPWrapper._make_request() (temporariamente):
```python
def _make_request(self, method, endpoint, data=None):
    # ... código existente ...
    response = self.session.request(...)
    
    if not response.ok:
        print(f"❌ ERROR {response.status_code}: {response.text}", flush=True)  # ← ADD ISTO
    
    return response.json() if response.ok else None
```

---

### Cenário 3: API retorna sucesso mas dados não mudaram

**Console da GUI**:
```
✅ Pessoa editada com sucesso! Resultado: {...}
📊 Dados após edição: {'id': 126, 'cpf': '12345678900', ...}  ← CPF NÃO MUDOU!

❌ cpf: solicitado '12345678910' mas permanece '12345678900'

⚠️ ALERTA: Algumas mudanças NÃO foram persistidas no backend!
   Tentando com PUT completo como fallback...
```

**Console do Django**:
```
🔵 PersonSerializer.update() CHAMADO
   Instance ID: 126
   Validated data: {'cpf': '12345678910', ...}
   💾 Salvando no banco de dados...
   ✅ Salvo! Verificação pós-save:
      cpf: 12345678910  ← AQUI SALVOU!
```

**⚠️ PROBLEMA ENCONTRADO**: A serializer salvou (`cpf: 12345678910`), mas o GET seguinte retorna valor antigo.

**Possíveis causas**:
1. Vários workers Django rodando e GET vai para outro processo com cache
2. Transação não foi commitada
3. PostgreSQL está retornando valor em cache

**Solução**: Adicionar `transaction.commit()` explícito em PersonSerializer.update():
```python
from django.db import transaction

def update(self, instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    transaction.commit()  # ← FORCE COMMIT
    instance.refresh_from_db()
    return instance
```

---

### Cenário 4: Erro 400 (Bad Request)

**Console da GUI**:
```
❌ Falha ao editar pessoa - resultado vazio
```

**Console do Django** (pode haver erro de validação):
```
⚠️ CPF já está cadastrado para outra pessoa
```

**Diagnóstico**: Seu novo CPF já está em uso por outra pessoa
**Solução**: Escolher um CPF diferente ou primeiro remover de outra pessoa

---

### Cenário 5: Erro 500 (Internal Server Error)

**Console da GUI**:
```
❌ Falha ao editar pessoa - resultado vazio
```

**Console do Django**:
```
ERROR: IntegrityError: ...
```

**Diagnóstico**: Erro no banco de dados (constraint violado, conexão perdida, etc)
**Solução**: Verificar logs completos do Django

---

## 🔧 COMO HABILITAR MAIS LOGS (DEBUG MODE)

### Em DatabaseHTTPWrapper.py - Adicione no `_make_request()`:

```python
def _make_request(self, method, endpoint, data=None):
    print(f"📤 DEBUG: METHOD={method}, ENDPOINT={endpoint}, DATA={data}", flush=True)
    
    # ... código existente ...
    
    response = self.session.request(method, self.base_url + endpoint, json=data, ...)
    
    print(f"📥 DEBUG: STATUS={response.status_code}, TEXT={response.text[:200]}", flush=True)
    
    return response.json() if response.ok else None
```

### Em Django - Habilite SQL logging:

**Em Web/gaia_backend/settings.py**:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # ← Mostra queries SQL
        },
    },
}
```

Depois você verá todas as queries SQL no console do Django:
```
(0.000) UPDATE "report_person" SET "cpf" = 12345678910 WHERE "id" = 126; args=[...]
```

---

## ✅ CHECKLIST DE DEBUG

- [ ] Verificar se console da GUI mostra `🔄 Enviando PATCH`
- [ ] Verificar se console do Django mostra `🔵 PersonSerializer.update() CHAMADO`
- [ ] Verificar se console do Django mostra `✅ Salvo!` com CPF correto
- [ ] Verificar se console da GUI mostra `✅ cpf: ANTES → DEPOIS` na validação
- [ ] Executar SQL direto: `SELECT cpf FROM report_person WHERE id=126`
- [ ] Verificar se não há erro 400 ou 500 na resposta
- [ ] Se tudo OK mas GUI ainda mostra CPF antigo, problema é no refresh da GUI

---

## 📞 CONCLUSÃO

Com os logs implementados, você consegue seguir exatamente onde o CPF se perde. Os logs apontam automaticamente para qual etapa do fluxo tem problema:

- **GUI logs** → Usa `📋`, `🔄`, `✅`, `❌` (color emoji)
- **Django logs** → Usa `🔵`, `💾`, `✅` (blue cirlce emoji)
- **Fluxo de validação** → Usa `🔎`, `📊` (magnifying glass, bar chart emoji)

Procure pela primeira linha `❌` (erro) - ela vai identificar exatamente donde empezaou o problema!
