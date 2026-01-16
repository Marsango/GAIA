#!/usr/bin/env python
"""
Simple test without special characters
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def login():
    response = requests.post(
        f"{BASE_URL}/api/login/cpf/",
        json={"cpf": "99988877700", "password": "123456"}
    )
    return response.json().get('access') if response.status_code == 200 else None

token = login()
if not token:
    print("FAIL: Login failed")
    exit(1)

print("OK: Login successful")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Test 1: Create address
print("\nStep 1: Creating address...")
addr_data = {
    "cep": "99999999",
    "rua": "Rua Debug",
    "numero": "999",
    "cidade": "Sao Paulo",
    "estado": "SP",
    "pais": "Brasil"
}
r = requests.post(f"{BASE_URL}/api/enderecos/", headers=headers, json=addr_data)
if r.status_code == 201:
    addr_id = r.json().get('id')
    print(f"OK: Address created ID {addr_id}")
else:
    print(f"FAIL: Address error {r.status_code}: {r.text[:100]}")
    exit(1)

# Test 2: Create person
print("\nStep 2: Creating person...")
from random import randint
person_data = {
    "name": f"Debug Person {randint(10000, 99999)}",
    "nascimento": "1990-01-15",
    "cpf": f"111{randint(100, 999)}{randint(100, 999)}{randint(100, 999)}{randint(10, 99)}",
    "email": f"debug{randint(10000, 99999)}@test.com",
    "phone_number": "(11) 99999-8888",
    "endereco": addr_id
}
r = requests.post(f"{BASE_URL}/api/pessoas/", headers=headers, json=person_data)
if r.status_code == 201:
    person_id = r.json().get('id')
    print(f"OK: Person created ID {person_id}")
else:
    print(f"FAIL: Person error {r.status_code}: {r.text[:100]}")
    exit(1)

# Test 3: Create propriedade
print("\nStep 3: Creating propriedade...")
prop_data = {
    "name": f"Debug Property {randint(10000, 99999)}",
    "registration_number": randint(1000000, 9999999),
    "proprietario_id": person_id,
    "endereco": addr_id
}
r = requests.post(f"{BASE_URL}/api/propriedades/", headers=headers, json=prop_data)
print(f"Response code: {r.status_code}")
if r.status_code == 201:
    prop_id = r.json().get('id')
    print(f"OK: Propriedade created ID {prop_id}")
elif r.status_code == 400:
    print(f"FAIL: Propriedade validation error: {r.text}")
    exit(1)
else:
    print(f"FAIL: Propriedade error {r.status_code}")
    if r.status_code == 500:
        print("ERROR: HTTP 500 detected!")
        if "ValueError" in r.text:
            print("ERROR: ValueError found!")
    print(f"Response: {r.text[:200]}")
    exit(1)

# Test 4: Create amostra
print("\nStep 4: Creating amostra...")
amostra_data = {
    "propriedade_id": prop_id,
    "numero_amostra": randint(5000, 9999),
    "data_coleta": str(date.today()),
    "ph": 6.5,
    "fosforo": 10.5,
    "potassio": 150,
    "materia_organica": 2.5,
    "argila": 25,
    "silte": 15,
    "areia": 60,
    "descricao": "Test amostra"
}
r = requests.post(f"{BASE_URL}/api/amostras/criar_simples/", headers=headers, json=amostra_data)
if r.status_code == 201:
    amostra_id = r.json().get('id')
    print(f"SUCCESS: Amostra created ID {amostra_id}")
    print("\nALL TESTS PASSED!")
else:
    print(f"FAIL: Amostra error {r.status_code}")
    if r.status_code == 500 and "ValueError" in r.text:
        print("ERROR: ValueError found in HTTP 500!")
    print(f"Response: {r.text[:300]}")

#test 5: Edit Person
print("\nStep 5: Editing person...")
updated_person_data = {
    "name": f"Debug Person Updated {randint(10000, 99999)}",
    "nascimento": "1991-01-15",
    "cpf": person_data["cpf"],
    "email": f"debug_updated{randint(10000, 99999)}@test.com",
    "phone_number": "(11) 98888-7777",
    "endereco": addr_id
}
r = requests.put(f"{BASE_URL}/api/pessoas/{person_id}/", headers=headers, json=updated_person_data)
if r.status_code == 200:
    print(f"OK: Person updated ID {person_id}")
else:
    print(f"FAIL: Person update error {r.status_code}: {r.text[:100]}")
    exit(1)

#test 6: Edit Address
print("\nStep 6: Editing address...")
updated_addr_data = {
    "cep": "88888888",
    "rua": "Rua Debug Updated",
    "numero": "888",
    "cidade": "Rio de Janeiro",
    "estado": "RJ",
    "pais": "Brasil"
}
r = requests.put(f"{BASE_URL}/api/enderecos/{addr_id}/", headers=headers, json=updated_addr_data)
if r.status_code == 200:
    print(f"OK: Address updated ID {addr_id}")
else:
    print(f"FAIL: Address update error {r.status_code}: {r.text[:100]}")
    exit(1)

#test 7: Edit Propriedade
print("\nStep 7: Editing propriedade...")
updated_prop_data = {
    "name": f"Debug Property Updated {randint(10000, 99999)}",
    "registration_number": prop_data["registration_number"] + 1,
    "proprietario_id": person_id,
    "endereco": addr_id
}
r = requests.put(f"{BASE_URL}/api/propriedades/{prop_id}/", headers=headers, json=updated_prop_data)
print(f"Response code: {r.status_code}")
if r.status_code == 200:
    print(f"OK: Propriedade updated ID {prop_id}")
else:
    print(f"FAIL: Propriedade update error {r.status_code}: {r.text[:100]}")
    exit(1)

#test 8: Edit Amostra
print("\nStep 8: Editing amostra...")
updated_amostra_data = {
    "propriedade_id": prop_id,
    "numero_amostra": amostra_data["numero_amostra"] + 1,
    "data_coleta": str(date.today()),
    "ph": 7.0,
    "fosforo": 12.0,
    "potassio": 160,
    "materia_organica": 3.0,
    "argila": 30,
    "silte": 20,
    "areia": 50,
    "descricao": "Updated test amostra"
}
r = requests.put(f"{BASE_URL}/api/amostras/{amostra_id}/", headers=headers, json=updated_amostra_data)
if r.status_code == 200:
    print(f"OK: Amostra updated ID {amostra_id}")
    print("\nALL EDIT TESTS PASSED!")
else:
    print(f"FAIL: Amostra update error {r.status_code}: {r.text[:100]}")
    exit(1)