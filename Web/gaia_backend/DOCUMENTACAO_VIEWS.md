# 📚 Documentação Completa - authentication/views.py

## 📋 Índice

1. [Importações](#importações-e-configuração)
2. [Estrutura de Segurança](#estrutura-de-segurança)
3. [Endpoints de Login](#endpoints-de-login)
4. [Endpoints de Usuário](#endpoints-de-usuário)
5. [Endpoints de Admin](#endpoints-de-admin)
6. [Endpoints de Sincronização](#endpoints-de-sincronização)

---

## 🔧 Importações e Configuração

```python
# rest_framework: Framework REST para Django
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# simplejwt: Tokens JWT seguros (access + refresh)
from rest_framework_simplejwt.tokens import RefreshToken

# rate-limit: Proteção contra força bruta
from django_ratelimit.decorators import ratelimit

# django: Autenticação, email, validação de senha
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password

# security.py: Funções de proteção progressiva
from .security import (
    record_login_attempt,      # Registra tentativa de login
    get_failed_attempts,       # Conta falhas do IP/CPF
    get_login_security_status, # Retorna: {require_captcha, failed_attempts}
    should_block_login,        # Verifica se está permanentemente bloqueado
    create_captcha_challenge,  # Gera desafio matemático
    verify_captcha,            # Valida resposta do CAPTCHA
    clear_failed_attempts      # Limpa histórico após sucesso
)
```

---

## 🔒 Estrutura de Segurança

### Permission Classes (Autorização)

| Classe            | Acesso                           | Usado em                              |
| ----------------- | -------------------------------- | ------------------------------------- |
| `AllowAny`        | Qualquer pessoa, não autenticada | Login, Forgot Password, Register      |
| `IsAuthenticated` | Usuário logado                   | Logout, Change Password, Current User |
| `IsAdminUser`     | Apenas is_staff=True             | Sync, Delete, Register, List Usuarios |

### Proteção contra Força Bruta (security.py)

```
Tentativas de Login:
├─ 0-2 falhas  → Sem restrição (comportamento normal)
├─ 3-4 falhas  → Delay de 30s entre tentativas
├─ 5+ falhas   → Requer CAPTCHA matemático
└─ Permanente  → Bloqueado por 24 horas (tentativas excessivas)
```

### Tokens JWT (httpOnly Cookies)

```
Access Token:
├─ Válido por: 1 hora
├─ Usado em: Todas as requisições autenticadas
└─ Armazenado em: Cookie httpOnly (não acessível via JavaScript)

Refresh Token:
├─ Válido por: 7 dias
├─ Usado em: Renovar access_token expirado
└─ Armazenado em: Cookie httpOnly
```

---

## 🔐 Endpoints de Login

### `login_with_cpf_secure(request)` - POST /api/login/cpf/secure/

**Função:** Login com CPF + Senha + Proteção Progressiva

**Fluxo:**

```
1. Cliente envia: {"cpf": "12345678900", "password": "senha123"}
2. Sistema verifica: IP do cliente
3. Sistema conta: tentativas de falha nos últimos 60 min
4. Se < 5 falhas: Continua normalmente
5. Se ≥ 5 falhas: Requer CAPTCHA
   └─ Cliente envia: {"cpf": "...", "password": "...", "captcha_token": "...", "captcha_answer": "..."}
6. Se senha correta:
   ├─ Gera access_token (1 hora)
   ├─ Gera refresh_token (7 dias)
   ├─ Limpa histórico de falhas
   └─ Retorna tokens em httpOnly cookies
7. Se senha incorreta:
   ├─ Registra tentativa de falha
   ├─ Incrementa contador
   ├─ Se ≥ 5 falhas: Retorna CAPTCHA challenge
   └─ Retorna erro 401
```

**Exemplo de Requisição:**

```json
{
  "cpf": "123.456.789-00",
  "password": "MinhaSeNha123!",
  "captcha_token": "abc123...", // opcional (se requer CAPTCHA)
  "captcha_answer": "42" // opcional (se requer CAPTCHA)
}
```

**Resposta de Sucesso (200):**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "cpf": "12345678900",
    "is_staff": false,
    "primeiro_acesso": false
  }
}
```

**Resposta com CAPTCHA Required (403):**

```json
{
  "require_captcha": true,
  "captcha": {
    "token": "def456...",
    "question": "2 + 3 = ?",
    "image_url": "data:image/png;base64..."
  },
  "message": "Muito muitas tentativas. Por favor, resolva o CAPTCHA."
}
```

### `login_with_cnpj_secure(request)` - POST /api/login/cnpj/secure/

**Idêntico ao CPF, mas para Empresas:**

- CNPJ em vez de CPF
- Sem caracteres especiais (12345678000190)
- Mesmo fluxo de securitye CAPTCHA

---

## 👤 Endpoints de Usuário

### `current_user(request)` - GET /api/current-user/

**Função:** Retorna dados do usuário logado

**Requer:** IsAuthenticated (qualquer usuário logado)

**Resposta:**

```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf": "12345678900",
  "email": "joao@email.com",
  "first_name": "João",
  "last_name": "Silva",
  "is_staff": false,
  "primeiro_acesso": false
}
```

**Uso no Frontend:**

- Exibir nome na barra de navegação
- Verificar se é admin (mostrar menu admin)
- Verificar se é primeiro acesso (forçar mudança de senha)

---

### `change_password(request)` - POST /api/change-password/

**Função:** Alterar senha do usuário logado

**Requer:** IsAuthenticated

**Validações:**

- ✅ Mínimo 8 caracteres
- ✅ Não apenas números
- ✅ Não semelhante ao CPF/email
- ✅ Não é senha comum (12345678, password, etc.)

**Requisição:**

```json
{
  "old_password": "senhaAnterior123!",
  "new_password": "novaSenha456!"
}
```

**Resposta de Sucesso (200):**

```json
{
  "message": "Senha alterada com sucesso."
}
```

**Efeito Secundário:**

- `usuario.primeiro_acesso` é marcado como `False`
- (Obrigatório na primeira vez: força mudança de senha)

---

### `logout_view(request)` - POST /api/logout/

**Função:** Fazer logout (remover sessão)

**Requer:** IsAuthenticated

**O que faz:**

1. Remove cookie `access_token`
2. Remove cookie `refresh_token`
3. Retorna mensagem de sucesso

**Resposta:**

```json
{
  "message": "Logout realizado com sucesso"
}
```

---

### `forgot_password(request)` - POST /api/forgot-password/

**Função:** Recuperar senha esquecida

**Requer:** AllowAny (sem autenticação)

**Fluxo:**

```
1. Usuário envia: {"email": "joao@email.com"}
2. Sistema: Procura usuario com esse email
3. Se encontrar:
   ├─ Gera nova senha aleatória (12 caracteres)
   ├─ Define primeiro_acesso = True
   ├─ Envia email com senha temporária
   └─ Retorna mensagem genérica
4. Se não encontrar:
   └─ Retorna mesma mensagem genérica (por segurança)
```

**Segurança:** Não revela se email existe ou não no banco

---

## 🔑 Endpoints de Admin

### `register_client_email(request)` - POST /api/register/client/

**Função:** Admin cadastra cliente (Pessoa Física)

**Requer:** IsAdminUser

**Fluxo:**

```
1. Admin envia: email, CPF, first_name, last_name (opção), telefone (opcional)
2. Sistema: Valida email/CPF únicos
3. Sistema: Cria usuario com senha aleatória (12 chars)
4. Sistema: Carrega template de email do banco
5. Sistema: Substitui {nome}, {senha}, {tipo_documento="CPF"}, {email}
6. Sistema: Envia email para o novo usuario
7. Sistema: Retorna sucesso (201)
```

**Requisição:**

```json
{
  "email": "joao@email.com",
  "cpf": "123.456.789-00",
  "first_name": "João",
  "last_name": "Silva",
  "phone_number": "(11) 98765-4321"
}
```

**Resposta:**

```json
{
  "message": "Usuário criado e e-mail enviado."
}
```

**Cliente recebe email:**

```
Olá João,

Suas credenciais de acesso:
Login: 12345678900 (CPF)
Senha: xYz9...abC1pQ (aleatória)

Por favor, altere sua senha no primeiro acesso.
```

---

### `register_company_email(request)` - POST /api/register/company/

**Idêntico a register_client_email, mas:**

- CNPJ em vez de CPF
- {tipo_documento="CNPJ"}
- Login com CNPJ (sem máscara)

---

### `list_usuarios(request)` - GET /api/usuarios/

**Função:** Listar todos os usuários cadastrados

**Requer:** IsAdminUser

**Query Params (opcionais):**

```
GET /api/usuarios/?cpf=123&name=João
```

**Resposta:**

```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "username": "12345678900",
      "name": "João Silva",
      "email": "joao@email.com",
      "cpf": "12345678900",
      "telefone": "(11) 98765-4321",
      "is_staff": false,
      "is_active": true,
      "data_criacao": "2024-01-15T10:30:00Z"
    },
    ...
  ]
}
```

---

### `delete_usuario(request)` - DELETE /api/usuarios/

**Função:** Deletar um usuario pelo CPF

**Requer:** IsAdminUser

**Request:**

```
DELETE /api/usuarios/?cpf=12345678900
ou
DELETE /api/usuarios/
Body: {"cpf": "12345678900"}
```

**Resposta:**

```json
{
  "message": "Usuário excluído com sucesso."
}
```

**⚠️ PERMANENTE:** Esta ação não pode ser desfeita!

---

### `sync_usuario(request)` - POST /api/sync/usuario/

**Função:** Software desktop cria novo usuario

**Requer:** IsAdminUser

**Diferença vs register_client_email:**

- `register_client_email`: EnVIA EMAIL com senha aleatória
- `sync_usuario`: Recebe senha no body (o software envia)

**Requisição:**

```json
{
  "cpf": "12345678900",
  "email": "joao@email.com",
  "first_name": "João",
  "last_name": "Silva",
  "password": "senhaQt123!"
}
```

**Resposta:**

```json
{
  "id": 1,
  "status": "created",
  "message": "Usuário criado com sucesso",
  "cpf": "12345678900",
  "email": "joao@email.com",
  "name": "João Silva"
}
```

**Erros possíveis:**

- 409 Conflict: CPF já existe
- 409 Conflict: Email já existe

---

## 🔄 Endpoints de Sincronização

### `sync_usuario_by_cpf(request)` - PATCH /api/sync/usuario/cpf/

**Função:** Sincronizar Usuario quando Person (Pessoa Física) é editada

**Requer:** IsAdminUser

**Fluxo:**

```
1. Software desktop edita Person (nome, CPF, email, telefone)
2. Software chama: PATCH /api/sync/usuario/cpf/
3. Sistema: Localiza Usuario pelo CPF
4. Sistema: Atualiza campos fornecidos
5. Sistema: Salva e retorna sucesso
```

**Requisição:**

```json
{
  "cpf": "12345678900",
  "email": "joao.novo@email.com",
  "first_name": "João Atualizado",
  "telefone": "(11) 99999-8888",
  "new_cpf": "98765432100" // opcional (mudar CPF)
}
```

**Resposta:**

```json
{
  "id": 1,
  "username": "12345678900",
  "email": "joao.novo@email.com",
  "first_name": "João Atualizado",
  "telefone": "(11) 99999-8888",
  "updated_fields": ["email", "first_name", "telefone"]
}
```

**Campos atualizáveis:**

- `email`: Novo email
- `first_name`: Novo nome
- `last_name`: Novo sobrenome (opcional)
- `telefone`: Novo telefone
- `new_cpf`: Novo CPF (renomeia username também)

---

### `sync_usuario_by_cnpj(request)` - PATCH /api/sync/usuario/cnpj/

**Idêntico ao CPF, mas para Empresa (PJ)**

- CNPJ em vez de CPF
- `new_cnpj` em vez de `new_cpf`

---

### `delete_usuario_by_cpf(request)` - DELETE /api/delete/usuario/cpf/

**Função:** Deletar Usuario (chamado quando Person é deletada)

**Requer:** IsAdminUser

**Request:**

```
DELETE /api/delete/usuario/cpf/?cpf=12345678900
ou
Body: {"cpf": "12345678900"}
```

**Resposta:**

```json
{
  "message": "Usuario com CPF 12345678900 deletado com sucesso",
  "id": 1
}
```

**⚠️ PERMANENTE:** Deleta usuário e todas as credenciais de login

---

### `delete_usuario_by_cnpj(request)` - DELETE /api/delete/usuario/cnpj/

**Idêntico ao CPF, mas para empresas**

---

## 🧪 Endpoints de Teste/Debug

### `test_send_email(request)` - POST /api/test-email/

**Função:** Testar se o email está configurado corretamente

**Requer:** IsAdminUser

**Requisição:**

```json
{
  "email": "seu_email@gmail.com"
}
```

**Imprime no console:**

```
Backend SMTP: smtp.gmail.com
Porta: 587
TLS: True
Resultado: Email enviado com sucesso (num_sent=1)
```

**Útil para debugar:**

- Credenciais SMTP incorretas
- Firewall bloqueando porta 587
- Config de settings.py errada

---

### `manage_email_template(request)` - GET/POST /api/email-template/

**GET:** Retorna template atual do banco

**POST:** Atualiza template

**Placeholders disponíveis:**

```
{nome}             - Nome do usuário/empresa
{senha}            - Senha temporária
{email}            - Email da conta
{tipo_documento}   - "CPF" ou "CNPJ"
```

**Exemplo de Template:**

```
Olá {nome},

Bem-vindo ao GAIA!

Seus dados de acesso:
Login (CPF/CNPJ): {tipo_documento}
Senha Temporária: {senha}

Por favor, altere sua senha no primeiro acesso.

Suporte: suporte@gaia.com
```

---

## 🔐 Resumo de Segurança

| Aspecto               | Implementação                                   |
| --------------------- | ----------------------------------------------- |
| **Autenticação**      | JWT (access + refresh tokens), httpOnly cookies |
| **Autorização**       | AllowAny, IsAuthenticated, IsAdminUser          |
| **Rate Limiting**     | 6 tentativas/minuto por IP                      |
| **Força Bruta**       | Bloqueio progressivo com CAPTCHA                |
| **Força de Senha**    | Validação Django + min 8 chars                  |
| **Emails**            | SMTP seguro, templates customizáveis            |
| **Primeiro Acesso**   | Força mudança de senha obrigatória              |
| **Logout**            | Remove cookies httpOnly                         |
| **Senhas Aleatórias** | 12 caracteres, hash bcrypt                      |
