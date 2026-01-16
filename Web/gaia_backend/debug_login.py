# teste_rapido.py
print("=== TESTE RÁPIDO DO LOGIN ===")

import requests

BASE_URL = "http://localhost:8000"

# Testar login com as informações CORRETAS
print("\n1. Testando login...")
response = requests.post(
    f"{BASE_URL}/api/token/",
    json={"cpf": "99988877700", "password": "soft123456"},
    timeout=10
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    token = data.get("access")
    print(f"✅ LOGIN BEM-SUCEDIDO!")
    print(f"Token: {token[:50]}...")
    
    # Testar token
    print("\n2. Testando token...")
    headers = {"Authorization": f"Bearer {token}"}
    response2 = requests.get(
        f"{BASE_URL}/api/health/",
        headers=headers,
        timeout=5
    )
    print(f"Status do health check: {response2.status_code}")
    
    # Testar endpoint protegido
    print("\n3. Testando endpoint protegido...")
    response3 = requests.get(
        f"{BASE_URL}/api/propriedades/",
        headers=headers,
        timeout=5
    )
    print(f"Status de propriedades: {response3.status_code}")
    
    if response3.status_code == 200:
        print("✅ Tudo funcionando perfeitamente!")
    else:
        print(f"⚠️  Problema com autenticação. Resposta: {response3.text[:200]}")
        
else:
    print(f"❌ Falha no login")
    print(f"Resposta: {response.text[:200]}")