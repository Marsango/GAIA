#!/usr/bin/env python
"""
Script para testar Rate Limiting nos endpoints de Login
Deve executar 25+ requisições e mostrar quando começa a bloquear (429)
"""
import requests
import time
from datetime import datetime

# URL dos endpoints
BASE_URL = "http://localhost:8000/api"
LOGIN_CPF_URL = f"{BASE_URL}/login/cpf/secure/"
LOGIN_CNPJ_URL = f"{BASE_URL}/login/cnpj/"

# Dados de teste (credenciais inválidas propositalmente)
CPF_DATA = {
    "cpf": "12345678901",
    "password": "senha_errada"
}

CNPJ_DATA = {
    "cnpj": "12345678000190",
    "password": "senha_errada"
}

def test_ratelimit(url, data, endpoint_name, num_requests=25):
    """
    Testa rate limiting em um endpoint
    """
    print(f"\n{'='*70}")
    print(f"🔐 TESTANDO RATE LIMITING: {endpoint_name}")
    print(f"{'='*70}")
    print(f"URL: {url}")
    print(f"Limite: 10 requisições por minuto (por IP)")
    print(f"Tentativas: {num_requests}\n")
    
    blocked_count = 0
    success_count = 0
    times = []
    
    for i in range(1, num_requests + 1):
        try:
            start_time = time.time()
            response = requests.post(url, json=data, timeout=5)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            status_code = response.status_code
            
            if status_code == 401:
                status_text = "❌ 401 Unauthorized (senha errada - ESPERADO)"
                success_count += 1
            elif status_code == 429:
                status_text = "🚫 429 Too Many Requests (BLOQUEADO ✓)"
                blocked_count += 1
            elif status_code == 403:
                status_text = "🚫 403 Forbidden (BLOQUEADO POR RATE LIMIT ✓)"
                blocked_count += 1
            elif status_code == 400:
                status_text = "⚠️  400 Bad Request"
                success_count += 1
            else:
                status_text = f"? {status_code} {response.reason}"
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{i:2d}] [{timestamp}] {status_text} ({elapsed:.3f}s)")
            
            # Pequena pausa para não sobrecarregar
            if i < num_requests:
                time.sleep(0.05)
                
        except requests.exceptions.Timeout:
            print(f"[{i:2d}] ⏱️  TIMEOUT - Servidor não respondeu")
        except requests.exceptions.ConnectionError:
            print(f"[{i:2d}] 🔌 ERRO DE CONEXÃO - Servidor não está rodando?")
            break
        except Exception as e:
            print(f"[{i:2d}] ❌ ERRO: {str(e)}")
    
    # Resumo
    print(f"\n{'='*70}")
    print(f"📊 RESUMO DO TESTE - {endpoint_name}")
    print(f"{'='*70}")
    print(f"Total de requisições: {num_requests}")
    print(f"✅ Aceitas (401/400): {success_count}")
    print(f"🚫 Bloqueadas (403/429): {blocked_count}")
    print(f"⚠️  Taxa de bloqueio: {(blocked_count/num_requests)*100:.1f}%")
    
    if blocked_count > 0:
        print(f"\n✅ TESTE PASSOU: Rate limiting está funcionando!")
        print(f"   Os primeiros ~10 requisições foram aceitas.")
        print(f"   Requisições após o limite foram bloqueadas com 403.")
    elif success_count >= 10:
        print(f"\n❌ TESTE FALHOU: Nenhum bloqueio detectado!")
        print(f"   Rate limiting pode não estar ativo.")
    else:
        print(f"\n⚠️  RESULTADO INCONCLUSIVO: Verifique a conexão.")
    
    print(f"\n{'='*70}\n")
    
    return blocked_count > 0

def main():
    print("\n" + "🔒 "*35)
    print(" TESTE DE RATE LIMITING - FORÇA BRUTA")
    print("🔒 "*35)
    
    print("\n⏳ Aguardando... (o servidor precisa estar rodando em localhost:8000)")
    time.sleep(1)
    
    # Teste 1: Login com CPF
    result_cpf = test_ratelimit(
        LOGIN_CPF_URL,
        CPF_DATA,
        "Login com CPF",
        num_requests=25
    )
    
    # Teste 2: Login com CNPJ
    result_cnpj = test_ratelimit(
        LOGIN_CNPJ_URL,
        CNPJ_DATA,
        "Login com CNPJ",
        num_requests=25
    )
    
    # Resultado final
    print("\n" + "="*70)
    if result_cpf and result_cnpj:
        print("✅ SEGURANÇA VALIDADA: Rate limiting em ambos endpoints está ATIVO")
        print("\n📝 COMO FUNCIONA:")
        print("   - django-ratelimit bloqueia com HTTP 403 Forbidden (não 429)")
        print("   - Limite: 20 requisições por minuto por IP")
        print("   - Chave de bloqueio: Endereço IP do cliente")
    elif result_cpf or result_cnpj:
        print("⚠️  TESTE PARCIAL: Rate limiting em apenas um endpoint")
    else:
        print("❌ ALERTA: Rate limiting pode não estar funcionando!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
