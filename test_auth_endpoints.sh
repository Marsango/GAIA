#!/bin/bash
# Script para testar endpoints de autenticação

BASE_URL="http://localhost:8000/api"

echo "==============================================="
echo "Testando Endpoints de Autenticação"
echo "==============================================="

# 1. Teste de Login com CPF
echo ""
echo "1. Teste de Login com CPF:"
echo "---"
curl -s -X POST "$BASE_URL/auth/login/cpf/" \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "password": "senha123"
  }' \
  -v 2>&1 | grep -E "HTTP|access_token|refresh_token|Set-Cookie"

# 2. Teste de Refresh Token
echo ""
echo "2. Teste de Refresh Token (sem autenticação):"
echo "---"
curl -s -X POST "$BASE_URL/token/refresh/" \
  -H "Content-Type: application/json" \
  -v 2>&1 | grep -E "HTTP|error"

# 3. Teste de Logout
echo ""
echo "3. Teste de Logout (sem autenticação):"
echo "---"
curl -s -X POST "$BASE_URL/logout/" \
  -H "Content-Type: application/json" \
  -v 2>&1 | grep -E "HTTP"

echo ""
echo "==============================================="
echo "Testes Completos"
echo "==============================================="
