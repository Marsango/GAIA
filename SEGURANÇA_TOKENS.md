# Documentação de Segurança de Tokens - Frontend

## ✅ Alterações Implementadas (2 de Março de 2026)

### 1. **Padronização de Nomes de Tokens**

#### Antes (INCONSISTENTE):

- Login armazenava: `"token"` e `"refresh"`
- AdminPanel recuperava: `"token"` ✓ (coincidia)
- Amostras recuperava: `"access_token"` ✗ (NÃO ENCONTRAVA)
- useAuth armazenava: `"access_token"` e `"refresh_token"` (diferente)

#### Depois (PADRONIZADO):

Todos os componentes agora usam:

- **`access_token`** - Token JWT de acesso (válido por 60 minutos)
- **`refresh_token`** - Token de refresh (válido por 7 dias)
- **`access_token_expires`** - Timestamp de expiração em milissegundos

### 2. **Arquivos Atualizados**

| Arquivo                      | Alterações                                                                    |
| ---------------------------- | ----------------------------------------------------------------------------- |
| **Login/index.jsx**          | ✅ Armazena como `access_token` + `refresh_token` + timestamp de expiração    |
| **api.js**                   | ✅ Usa `access_token` + valida expiração antes de cada requisição             |
| **ChangePassword/index.jsx** | ✅ Recupera e remove corretamente `access_token`                              |
| **AdminPanel/index.jsx**     | ✅ Recupera como `access_token`                                               |
| **Header/index.jsx**         | ✅ Remove `access_token` + `refresh_token` + `access_token_expires` no logout |
| **PrivateRoute.jsx**         | ✅ Valida token expirado + redireciona para login                             |
| **Reports/index.jsx**        | ✅ Valida expiração ao carregar                                               |
| **Amostras/index.jsx**       | ✅ Remove fallback para `"token"`, usa apenas `access_token`                  |
| **useAuth.js**               | ✅ Hook retorna `isTokenExpired()` para validação                             |

### 3. **Validação de Expiração de Token**

#### Implementação em `api.js` (Interceptador de Request):

```javascript
const token = localStorage.getItem("access_token");
const expiresAt = localStorage.getItem("access_token_expires");

// Verifica se token expirou
if (expiresAt && Date.now() > parseInt(expiresAt)) {
  // Limpa todos os tokens
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("access_token_expires");
  localStorage.removeItem("user");
  window.location.href = "/login";
  return Promise.reject(new Error("Token expirado"));
}
```

#### Em `PrivateRoute.jsx`:

```javascript
if (token && expiresAt && Date.now() > parseInt(expiresAt)) {
  // Token expirou, faz logout automático
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("access_token_expires");
  localStorage.removeItem("user");
  return <Navigate to="/login" replace />;
}
```

### 4. **Tempo de Expiração**

- **Access Token**: 60 minutos
  - Armazenado em: `localStorage.getItem("access_token_expires")`
  - Valor: `Date.now() + 3600 * 1000` (milissegundos)
  - Validação: `Date.now() > parseInt(expiresAt)`

### 5. **Lógica de Logout Consistente**

Todos os componentes agora removem:

```javascript
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");
localStorage.removeItem("access_token_expires");
localStorage.removeItem("user");
```

---

## ⚠️ Problemas RESOLVIDOS

### **Bug Crítico #1**: Token não encontrado em Amostras/index.jsx

- **Causa**: Amostras procurava por `"access_token"` mas Login armazenava como `"token"`
- **Resultado**: Todas as requisições de amostras falhavam com token null
- **Solução**: Padronizar em `"access_token"`
- **Status**: ✅ RESOLVIDO

### **Bug #2**: Sem validação de expiração

- **Causa**: Token de 60 minutos era ignorado no frontend
- **Resultado**: Após 60 min, usuário recebia erro 401 silenciosamente
- **Solução**: Adicionar timestamp de expiração e validar antes de requisições
- **Status**: ✅ RESOLVIDO

### **Bug #3**: Inconsistência de logout

- **Causa**: Componentes removiam chaves diferentes
- **Resultado**: Tokens "fantasmas" permaneciam no localStorage
- **Solução**: Centralizar lógica de limpeza
- **Status**: ✅ RESOLVIDO

---

## 🔒 Problemas IDENTIFICADOS (Não Implementados Ainda)

### **CRITICAL - localStorage é XSS vulnerável**

- **Problema**: JavaScript pode acessar tokens em localStorage
- **Impacto**: Site XSS pode roubar token e fazer requisições
- **Solução Recomendada**: Migrar para httpOnly cookies (backend + frontend)
- **Prioridade**: ALTA (requer mudanças no backend Django)
- **Status**: 🔴 PENDENTE

### **HIGH - Sem refresh automático de token**

- **Problema**: Token expira em 60 min, sem renovação automática
- **Impacto**: Usuário será logout forçadamente após 60 min
- **Solução**: Implementar refresh token logic (chamar endpoint de refresh)
- **Prioridade**: ALTA
- **Status**: 🔴 PENDENTE

---

## 📋 Próximos Passos

### 1. **Testar padronização de tokens**

```bash
# Login e verificar no DevTools > Application > Storage > localStorage
# Deve conter: access_token, refresh_token, access_token_expires, user
```

### 2. **Implementar httpOnly Cookies** (após testes)

```python
# No backend (Django), configurar:
response.set_cookie(
    'access_token',
    value=token,
    httponly=True,  # ← Inacessível a JavaScript
    secure=True,    # ← Apenas HTTPS em produção
    samesite='Strict'
)
```

### 3. **Implementar refresh token automático**

```javascript
// Chamar endpoint /token/refresh/ antes de token expirar
if (Date.now() > parseInt(expiresAt) - 5 * 60 * 1000) {
  // 5 min antes
  const newToken = await api.post("/token/refresh/", {
    refresh: localStorage.getItem("refresh_token"),
  });
  localStorage.setItem("access_token", newToken.access);
  localStorage.setItem("access_token_expires", Date.now() + 3600 * 1000);
}
```

### 4. **Adicionar CORS restriction** (backend Django)

```python
# Alterar de DEBUG-based para lista explícita:
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  # dev
        "https://labsolos.com.br",  # produção
    ]
```

---

## 🧪 Teste Rápido de Segurança

### Verificar localStorage no DevTools:

```javascript
// Abrir Console do Navegador (F12 > Console) e executar:
console.log({
  access_token: localStorage.getItem("access_token"),
  refresh_token: localStorage.getItem("refresh_token"),
  expires_at: localStorage.getItem("access_token_expires"),
  expires_in:
    Math.round(
      (parseInt(localStorage.getItem("access_token_expires")) - Date.now()) /
        1000,
    ) + " segundos",
});
```

### Esperado:

```
{
  access_token: "eyJ0eXAiOiJKV1QiLCJhbG...",
  refresh_token: "eyJ0eXAiOiJKV1QiLCJhbG...",
  expires_at: "1740950400000",
  expires_in: "3599 segundos"  // ~60 minutos
}
```

---

## 📝 Histórico de Versões

| Data       | Versão | Alterações                                        |
| ---------- | ------ | ------------------------------------------------- |
| 2026-03-02 | 1.0    | ✅ Padronização de nomes + Validação de expiração |
| TBD        | 1.1    | 🔴 httpOnly Cookies (requer backend changes)      |
| TBD        | 2.0    | 🔴 Refresh token automático                       |
| TBD        | 2.1    | 🔴 CORS restriction em produção                   |

---

## 🔗 Referências

- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [OWASP Token Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [localStorage vs Cookies Security](https://stackoverflow.com/questions/27067251/where-to-store-jwt-in-browser)

---

**Última atualização**: 2 de março de 2026  
**Status**: Fase 1 concluída (Padronização de Tokens)  
**Próxima Fase**: httpOnly Cookies + Token Refresh
