import requests

BASE_URL = "http://localhost:8000"

CPF = "99988877700"      # ajuste se necessário
PASSWORD = "123456"          # ajuste se necessário


def login():
    resp = requests.post(
        f"{BASE_URL}/api/login/cpf/",
        json={
            "cpf": CPF,
            "password": PASSWORD
        }
    )

    print("🔑 LOGIN STATUS:", resp.status_code)
    print("🔑 LOGIN BODY:", resp.text)

    assert resp.status_code == 200
    return resp.json()["access"]


def test_insert_property_simple():
    token = login()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # ========= 1. Criar endereço =========
    endereco_payload = {
        "cep": "12345678",
        "rua": "Rua das Flores",
        "numero": "123",
        "cidade": "São Paulo",
        "estado": "SP",
        "pais": "Brasil"
    }

    endereco_resp = requests.post(
        f"{BASE_URL}/api/enderecos/",
        json=endereco_payload,
        headers=headers
    )

    print("📦 ENDERECO STATUS:", endereco_resp.status_code)
    print("📦 ENDERECO BODY:", endereco_resp.text)

    assert endereco_resp.status_code == 201

    endereco_id = endereco_resp.json()["id"]

    # ========= 2. Criar propriedade =========
    propriedade_payload = {
        "name": "Fazenda Teste",
        "endereco": endereco_id,
        "registration_number": 999999,
        "proprietario_id": 6  # ajuste se necessário
    }

    prop_resp = requests.post(
        f"{BASE_URL}/api/propriedades/",
        json=propriedade_payload,
        headers=headers
    )

    print("🏡 PROP STATUS:", prop_resp.status_code)
    print("🏡 PROP BODY:", prop_resp.text)

    assert prop_resp.status_code == 201

    prop_id = prop_resp.json()["id"]

    # ========= 3. Listar propriedades =========
    list_resp = requests.get(
        f"{BASE_URL}/api/propriedades/",
        headers=headers
    )

    print("📋 LIST STATUS:", list_resp.status_code)
    print("📋 LIST BODY:", list_resp.text)

    assert list_resp.status_code == 200

    propriedades = list_resp.json().get("results", [])

    encontrada = next(
        (
            p for p in propriedades
            if p["id"] == prop_id
            and p["name"] == "Fazenda Teste"
            and int(p["registration_number"]) == 999999
        ),
        None
    )

    assert encontrada is not None, "Propriedade não encontrada na listagem"

    print("✅ TESTE FINALIZADO COM SUCESSO")


if __name__ == "__main__":
    test_insert_property_simple()
