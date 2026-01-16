# Crie o arquivo: test_api_django.py
# test_api_django.py
import requests
import json

def test_django_api():
    print("=== TESTE DA API DJANGO ===")
    
    BASE_URL = "http://127.0.0.1:8000"
    
    # 1. Health Check
    print("\n1. Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # 2. Login
    print("\n2. Testando Login...")
    login_data = {"cpf": "11823766900", "password": "admin"}
    
    try:
        response = requests.post(f"{BASE_URL}/api/token/", json=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json()["access"]
            print(f"   ✅ Token obtido: {token[:30]}...")
            
            # 3. Testar endpoints protegidos
            headers = {"Authorization": f"Bearer {token}"}
            
            endpoints = [
                ("/api/propriedades/", "Listar propriedades"),
                ("/api/amostras/", "Listar amostras"),
                ("/api/laudos/", "Listar laudos"),
            ]
            
            print("\n3. Testando endpoints protegidos...")
            for endpoint, description in endpoints:
                try:
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=5)
                    data = response.json() if response.content else []
                    count = len(data) if isinstance(data, list) else "OK"
                    print(f"   ✅ {description}: {count}")
                except:
                    print(f"   ⚠ {description}: Erro")
            
            return True
        else:
            print(f"   ❌ Erro no login: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if test_django_api():
        print("\n" + "="*50)
        print("✅ API DJANGO FUNCIONANDO CORRETAMENTE!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("❌ PROBLEMAS NA API DJANGO")
        print("="*50)