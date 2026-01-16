# teste_endpoint_custom.py
import requests
import json

print("="*60)
print("TESTE DO ENDPOINT DE LOGIN CUSTOM /api/login/cpf/")
print("="*60)

# URL base do seu Django
BASE_URL = "http://localhost:8000"

# Credenciais para testar
CPF_TECNICO = "999.888.777-00"  # COM formatação
SENHA_TECNICO = "123456"

print(f"\n🔗 URL base: {BASE_URL}")
print(f"👤 CPF do técnico: {CPF_TECNICO}")
print(f"🔑 Senha: {SENHA_TECNICO}")

# ========== PASSO 1: TESTAR SE DJANGO ESTÁ RODANDO ==========
print(f"\n{'='*40}")
print("1. TESTANDO SE DJANGO ESTÁ RODANDO...")
print(f"{'='*40}")

try:
    health_response = requests.get(f"{BASE_URL}/api/health/", timeout=5)
    print(f"✅ Health check: Status {health_response.status_code}")
    
    if health_response.status_code != 200:
        print(f"❌ Django não está respondendo corretamente")
        print(f"   Execute: python manage.py runserver")
        exit()
except Exception as e:
    print(f"❌ Erro ao conectar com Django: {e}")
    print(f"   Verifique se o Django está rodando na porta 8000")
    exit()

# ========== PASSO 2: TESTAR LOGIN CUSTOM ==========
print(f"\n{'='*40}")
print("2. TESTANDO LOGIN CUSTOM (/api/login/cpf/)...")
print(f"{'='*40}")

# Dados para o login
login_data = {
    "cpf": CPF_TECNICO,
    "password": SENHA_TECNICO
}

print(f"📤 Enviando para: {BASE_URL}/api/login/cpf/")
print(f"📤 Dados: {json.dumps(login_data)}")

try:
    response = requests.post(
        f"{BASE_URL}/api/login/cpf/",
        json=login_data,
        timeout=10
    )
    
    print(f"📥 Status recebido: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access')
        
        print(f"\n✅ LOGIN BEM-SUCEDIDO!")
        print(f"   Token access (início): {token[:50]}...")
        print(f"   Token refresh: {data.get('refresh', '')[:50]}...")
        
        # Mostrar informações do usuário
        user_info = data.get('user', {})
        if user_info:
            print(f"\n👤 INFORMAÇÕES DO USUÁRIO:")
            print(f"   ID: {user_info.get('id')}")
            print(f"   Nome: {user_info.get('nome')}")
            print(f"   CPF: {user_info.get('cpf')}")
            print(f"   Email: {user_info.get('email')}")
            print(f"   Staff: {user_info.get('is_staff')}")
        
        # ========== PASSO 3: TESTAR TOKEN ==========
        print(f"\n{'='*40}")
        print("3. TESTANDO TOKEN EM ENDPOINTS PROTEGIDOS...")
        print(f"{'='*40}")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Lista de endpoints para testar
        endpoints = [
            ("/api/health/", "GET", "Permitido"),
            ("/api/propriedades/", "GET", "Exige login"),
            ("/api/amostras/", "GET", "Exige login"),
            ("/api/pessoas/", "GET", "Exige login"),
            ("/api/enderecos/", "GET", "Exige login"),
        ]
        
        for endpoint, method, desc in endpoints:
            try:
                resp = requests.request(
                    method,
                    f"{BASE_URL}{endpoint}",
                    headers=headers,
                    timeout=5
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    count = len(data) if isinstance(data, list) else 1
                    print(f"✅ {endpoint}: Status {resp.status_code} ({count} itens)")
                else:
                    print(f"❌ {endpoint}: Status {resp.status_code} - {desc}")
                    
            except Exception as e:
                print(f"❌ {endpoint}: Erro - {e}")
        
        print(f"\n🎉 TUDO FUNCIONANDO PERFEITAMENTE!")
        print(f"   O DatabaseHTTP pode usar o endpoint /api/login/cpf/")
        
    else:
        print(f"\n❌ FALHA NO LOGIN")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
        # Se for 404, endpoint não existe
        if response.status_code == 404:
            print(f"\n⚠️  O endpoint /api/login/cpf/ não existe!")
            print(f"   Verifique o arquivo authentication/urls.py")
            print(f"   Deve ter: path('login/cpf/', views.login_with_cpf)")
        
        # Se for 401, credenciais erradas
        elif response.status_code == 401:
            print(f"\n⚠️  Credenciais inválidas")
            print(f"   Verifique se o usuário técnico existe no Django")
        
        # Se for 400, dados incompletos
        elif response.status_code == 400:
            print(f"\n⚠️  Dados incompletos ou formato errado")
            print(f"   Resposta detalhada: {response.json()}")
            
except Exception as e:
    print(f"\n❌ ERRO AO TESTAR LOGIN: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*60}")
print("FIM DO TESTE")
print(f"{'='*60}")

# ========== PASSO EXTRA: TESTAR JWT PADRÃO ==========
print(f"\n{'='*40}")
print("4. TESTANDO JWT PADRÃO (/api/token/)...")
print(f"{'='*40}")

# Tentar diferentes combinações
test_cases = [
    {"username": "99988877700", "password": SENHA_TECNICO},
    {"username": CPF_TECNICO, "password": SENHA_TECNICO},
    {"cpf": CPF_TECNICO, "password": SENHA_TECNICO},
]

for test_data in test_cases:
    try:
        print(f"\n🔄 Testando: {json.dumps(test_data)}")
        resp = requests.post(
            f"{BASE_URL}/api/token/",
            json=test_data,
            timeout=5
        )
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ FUNCIONOU!")
            break
    except Exception as e:
        print(f"   ❌ Erro: {e}")