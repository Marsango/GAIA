# 🔧 Debug: Erro 400 Bad Request no Refresh Token

**Problema**: `POST /api/auth/token/refresh-cookie/ HTTP/1.1" 400`

---

## 🧪 Teste de Debug - Passo a Passo

### 1️⃣ Verificar se os Cookies Estão Sendo Recebidos

Após fazer login com sucesso, abra o DevTools (F12):

```javascript
// Console (F12 > Console):
document.cookie; // Deve conter 'access_token=...; refresh_token=...'
```

**Esperado**:

```
access_token=eyJ0eXA...; refresh_token=eyJ0eXA...; Path=/; HttpOnly
```

**Se vazio ou diferente** → Problema no backend ao setar cookies

---

### 2️⃣ Verificar Requisição Manual

No **Console** do navegador, após login:

```javascript
// Teste do refresh token manualmente
fetch("http://localhost:8000/api/auth/token/refresh-cookie/", {
  method: "POST",
  credentials: "include", // ← CRÍTICO: Envia cookies
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({}),
})
  .then((r) => {
    console.log("Status:", r.status);
    console.log("Headers:", r.headers);
    return r.json();
  })
  .then(console.log)
  .catch(console.error);
```

**Esperado**: Status 200 com `{message: "Token renovado com sucesso"}`

**Se Status 400**: Verificar resposta de erro

---

### 3️⃣ Ver Mensagem de Erro Completa

```bash
# No terminal do backend:
# Você deve ver a mensagem de erro completa, ex:
# [02/Mar/2026 14:52:14] POST /api/auth/token/refresh-cookie/ → 400
# TokenError: ...
```

---

## 🔍 Possíveis Causas & Soluções

### Causa 1: **Cookies Não Estão Sendo Recebidos**

**Sintoma**: `document.cookie` está vazio

**Solução - Verificar no Backend**:

```python
# Em authentication/views.py, no login_with_cpf():
# Adicionar debug:

print(f"🔐 Setting cookies...")
print(f"   access_token length: {len(access_token)}")
print(f"   refresh_token length: {len(refresh_token)}")

response = Response({'user': {...}})
response.set_cookie(...)
response.set_cookie(...)

# No terminal do Django, deve aparecer:
# 🔐 Setting cookies...
#    access_token length: 250+
#    refresh_token length: 250+
```

---

### Causa 2: **Cookies Não São Repassados na Requisição**

**Sintoma**: Cookies estão no DevTools mas `request.COOKIES.get('refresh_token')` retorna None

**Solução**: Verificar se axios está com `withCredentials: true`

```javascript
// Em api.js (linha 8):
const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true, // ← DEVE estar true
});
```

---

### Causa 3: **CORS Não Permitindo Credenciais**

**Sintoma**: Console error: `Credentials mode is 'include', but Access-Control-Allow-Credentials is missing`

**Solução**: Verificar settings.py

```python
# config/settings.py (por volta da linha 75):
CORS_ALLOW_CREDENTIALS = True  # ← DEVE estar True
CORS_ALLOWED_ORIGINS = [...]    # ← Frontend deve estar aqui
```

---

### Causa 4: **Token Inválido ou Expirado**

**Sintoma**: Status 400 com `{error: "Token inválido ou expirado"}`

**Solução**: O token foi gerado mas é inválido

```python
# Debug no backend:
# Em authentication/views.py → refresh_token_from_cookie():

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_from_cookie(request):
    refresh_token = request.COOKIES.get('refresh_token')

    # DEBUG:
    if not refresh_token:
        print("❌ refresh_token NÃO encontrado nos cookies")
    else:
        print(f"✅ refresh_token encontrado, length={len(refresh_token)}")

    # ... resto do código
```

---

## 🚀 Teste Completo de Login → Amostras

### Passo 1: Fazer Login

```bash
curl -X POST http://localhost:8000/api/auth/login/cpf/ \
  -H "Content-Type: application/json" \
  -d '{"cpf": "12345678901", "password": "senha123"}' \
  -v
```

**Esperado**:

```
HTTP/1.1 200 OK
Set-Cookie: access_token=...
Set-Cookie: refresh_token=...
```

### Passo 2: Fazer Requisição com Cookies

```bash
curl -X GET http://localhost:8000/api/propriedades/ \
  -H "Cookie: access_token=...; refresh_token=..." \
  -v
```

**Esperado**: HTTP/1.1 200 OK (ou 401 se token expirou, então fazer refresh)

### Passo 3: Renovar Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh-cookie/ \
  -H "Cookie: access_token=...; refresh_token=..." \
  -H "Content-Type: application/json" \
  -d '{}' \
  -v
```

**Esperado**: HTTP/1.1 200 OK com novo `access_token` em cookie

---

## 📋 Checklist de Debug

- [ ] `document.cookie` contém `access_token` e `refresh_token` após login
- [ ] `api.js` tem `withCredentials: true`
- [ ] `settings.py` tem `CORS_ALLOW_CREDENTIALS = True`
- [ ] `settings.py` tem `http://localhost:3000` (ou URL do frontend) em `CORS_ALLOWED_ORIGINS`
- [ ] Backend exibe "Setting cookies..." no login (adicione print para debug)
- [ ] Fetch manual em Console retorna 200 para `/token/refresh-cookie/`
- [ ] Não há erro CORS no console do navegador

---

## ❌ Se Ainda Não Funcionar

Forneça estes logs:

### 1. Terminal do Backend (após login):

```bash
# Colar output completo aqui
```

### 2. Console do Navegador (F12 >Console > Colar):

```javascript
console.log({
  cookies: document.cookie,
  localStorage: localStorage,
  apiBaseUrl: "http://localhost:8000/api/",
});
```

### 3. Network Tab (F12 > Network):

- Fazer requisição de login
- Procurar por request para `/auth/login/cpf/`
- Ver se `Set-Cookie` aparece em Response Headers

---

## 🛠️ Limpeza de Cookies para Restar

Se estiver preso em estado ruim, limpar cookies e tentar novamente:

```javascript
// Console:
document.cookie.split(";").forEach((c) => {
  const name = c.split("=")[0].trim();
  document.cookie = name + "=; max-age=0; path=/;";
});
localStorage.clear();
// Recarregar página: F5
```

---

**Próximas informações que ajudam no debug**:

1. Saída completa do login (curl ou network tab)
2. Se cookies estão sendo recebidos
3. Mensagem de erro exata do backend
