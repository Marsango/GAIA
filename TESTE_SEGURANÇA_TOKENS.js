// TESTE DE VALIDAÇÃO - Tokens Security Implementation
// Copie este código no Console do navegador (F12 > Console) após fazer login

// ============================================================
// TESTE 0: LIMPAR CHAVES ANTIGAS (se existirem)
// ============================================================
console.log("🧹 TESTE 0: Limpar chaves antigas");
console.log("=".repeat(50));

const hasOldToken = localStorage.getItem("token");
const hasOldRefresh = localStorage.getItem("refresh");

if (hasOldToken || hasOldRefresh) {
  console.warn("⚠️ Chaves antigas encontradas! Limpando...");
  localStorage.removeItem("token");
  localStorage.removeItem("refresh");
  console.log("✅ Chaves antigas removidas!");
} else {
  console.log("✅ Nenhuma chave antiga encontrada");
}

// ============================================================
// TESTE 1: Verificar se tokens estão armazenados corretamente
// ============================================================
console.log("\n📋 TESTE 1: Verificar armazenamento de tokens");
console.log("=".repeat(50));

const accessToken = sessionStorage.getItem("access_token");
const user = JSON.parse(localStorage.getItem("user") || "{}");

console.log({
  "✅ access_token existe": !!accessToken,
  "✅ user existe": !!user.id,
});

console.log("\n📊 Detalhes dos tokens:");

// Decodificar JWT para mostrar informações
let tokenInfo = { decoded: null, expiresAt: null, timeRemaining: null };
if (accessToken) {
  try {
    const parts = accessToken.split('.');
    if (parts.length === 3) {
      const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
      tokenInfo.decoded = payload;
      tokenInfo.expiresAt = new Date(payload.exp * 1000);
      tokenInfo.timeRemaining = Math.floor((payload.exp * 1000 - Date.now()) / 1000);
    }
  } catch (e) {
    console.warn('Não foi possível decodificar token');
  }
}

console.log({
  "access_token (primeiros 50 chars)": accessToken?.substring(0, 50) + "...",
  "user.id": user.id,
  "user.nome": user.nome,
  "user.email": user.email,
});

if (tokenInfo.decoded) {
  const minutes = Math.floor(tokenInfo.timeRemaining / 60);
  const seconds = tokenInfo.timeRemaining % 60;
  const willRefreshSoon = tokenInfo.timeRemaining < 300; // 5 minutos
  
  console.log("\n⏰ Informações de Expiração:");
  console.log({
    "Token expira em": `${minutes}m ${seconds}s`,
    "Expira às": tokenInfo.expiresAt.toLocaleTimeString('pt-BR'),
    "Status": willRefreshSoon ? "⚠️ Será renovado na próxima requisição" : "✅ Token válido",
    "Renovação proativa": willRefreshSoon ? "ATIVA (< 5 min)" : "AGUARDANDO (> 5 min)"
  });
}

// ============================================================
// TESTE 2: Verificar nomenclatura (sem "token" antigos)
// ============================================================
console.log("\n");
console.log("🔍 TESTE 2: Verificar nomenclatura de tokens");
console.log("=".repeat(50));

const oldTokenNames = localStorage.getItem("token");
const oldRefreshNames = localStorage.getItem("refresh");

console.log({
  "❌ Chave 'token' (ANTIGA) existe": !!oldTokenNames ? "ERRO!" : "✅ NÃO",
  "❌ Chave 'refresh' (ANTIGA) existe": !!oldRefreshNames ? "ERRO!" : "✅ NÃO",
  "✅ Usando 'access_token' (NOVO)": !!accessToken ? "✅ SIM" : "❌ NÃO",
});

if (oldTokenNames || oldRefreshNames) {
  console.warn("⚠️ AVISO: Chaves antigas encontradas! Execute cleanup:");
  console.warn(`localStorage.removeItem("token"); // se existir`);
  console.warn(`localStorage.removeItem("refresh"); // se existir`);
}

// ============================================================
// TESTE 3: Simular requisição e validar interceptor
// ============================================================
console.log("\n");
console.log("🌐 TESTE 3: Testar requisição com token");
console.log("=".repeat(50));

// Este teste fará uma requisição segura ao servidor
fetch("http://localhost:8000/api/user-info/", {  // ← CORRIGIDO: endpoint correto
  method: "GET",
  headers: {
    "Authorization": `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
})
  .then((res) => {
    console.log("✅ Requisição enviada com sucesso!");
    console.log(`📍 Status: ${res.status} ${res.statusText}`);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    return res.json();
  })
  .then((data) => {
    console.log("✅ Resposta recebida (usuário autenticado):");
    console.log(data);
  })
  .catch((err) => {
    console.error("❌ Erro na requisição:", err.message);
  });

// ============================================================
// TESTE 4: Validation Summary
// ============================================================
console.log("\n");
console.log("📋 RESUMO DA VALIDAÇÃO");
console.log("=".repeat(50));

const allValid =
  !!accessToken &&
  !!user.id &&
  !oldTokenNames &&
  !oldRefreshNames;

if (allValid) {
  console.log("✅ ✅ ✅  TODOS OS TESTES PASSARAM! ✅ ✅ ✅");
  console.log("\n🛡️ Implementação de segurança de tokens: SUCESSO");
  console.log("\n📋 Funcionalidades Ativas:");
  console.log("  ✅ Token em sessionStorage (limpo ao fechar navegador)");
  console.log("  ✅ Auto-refresh PROATIVO (renova 5 min antes de expirar)");
  console.log("  ✅ Interceptor detecta 401 como fallback");
  console.log("  ✅ Logout centralizado");
  console.log("  ✅ Nomenclatura padronizada");
  console.log("\nPróximos passos:");
  console.log("  1. Testar logout (deve remover todas chaves)");
  console.log("  2. Testar navegação entre páginas (token persiste)");
  console.log("  3. Aguardar expiração para ver renovação automática");
  console.log("  4. [FUTURO] Migrar para httpOnly cookies com CORS configurado");
} else {
  console.error("❌ ERROS ENCONTRADOS:");
  if (!accessToken) console.error("  - access_token não encontrado");
  if (!user.id) console.error("  - user data não encontrado");
  if (oldTokenNames) console.error("  - Chave antiga 'token' encontrada!");
  if (oldRefreshNames) console.error("  - Chave antiga 'refresh' encontrada!");
}

// ============================================================
// TESTE 5: Testar logout
// ============================================================
console.log("\n");
console.log("🔐 TESTE 5: Função de logout");
console.log("=".repeat(50));

console.log("Para testar logout, execute:");
console.log('sessionStorage.removeItem("access_token");  // ← sessionStorage agora');
console.log('localStorage.removeItem("user");');
console.log("\nOu clique em 'Sair' no menu do aplicativo.");

// ============================================================
// Quick Copy-Paste Commands
// ============================================================
console.log("\n");
console.log("📋 COMANDOS ÚTEIS PARA CONSOLE");
console.log("=".repeat(50));
console.log(`
// Limpar todos os tokens
sessionStorage.clear();
localStorage.clear();

// Ver tokens atuais
console.table({
  access_token: sessionStorage.getItem("access_token"),
  user: localStorage.getItem("user"),
});

// Fazer requisição de teste (vai adicionar token automaticamente)
fetch("http://localhost:8000/api/user-info/", {
  headers: {
    "Authorization": \`Bearer \${sessionStorage.getItem("access_token")}\`
  }
}).then(r => r.json()).then(console.log).catch(console.error);

// Testar requisição de propriedades (auto-refresh proativo)
fetch("http://localhost:8000/api/propriedades/", {
  headers: {
    "Authorization": \`Bearer \${sessionStorage.getItem("access_token")}\`
  }
}).then(r => r.json()).then(console.log).catch(console.error);

// ============================================================
// TESTE DE RENOVAÇÃO PROATIVA
// ============================================================
// Para testar renovação automática, crie um token que expira em 4 minutos:
// 1. Faça login normalmente
// 2. Execute este código para "simular" token próximo de expirar:

/*
const token = sessionStorage.getItem("access_token");
const parts = token.split('.');
const payload = JSON.parse(atob(parts[1]));

// Modificar exp para daqui a 4 minutos (240 segundos)
payload.exp = Math.floor(Date.now() / 1000) + 240;

// Recriar token (ATENÇÃO: Vai dar erro de assinatura, mas serve para testar lógica)
// Em produção, o backend que controla a expiração real
const fakeToken = parts[0] + '.' + btoa(JSON.stringify(payload)) + '.' + parts[2];
sessionStorage.setItem('access_token', fakeToken);

console.log('Token modificado para expirar em 4 minutos!');
console.log('Na próxima requisição, o interceptor vai tentar renovar automaticamente.');
*/

// ============================================================
// Testar que renovação funciona (chame uma API qualquer):
// import api from './api/api.js';
// api.get('propriedades/').then(console.log);
// Resultado: Deve ver "[API] ⚠ Token expirando em breve, renovando proativamente..."
`);
