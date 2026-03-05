#!/usr/bin/env python
"""
Teste de escopo de autorização para ADM x usuário comum.

Objetivo:
- Validar que endpoints de administração retornam 403 para usuário comum
- Validar que os mesmos endpoints retornam sucesso para usuário admin

Exemplo de uso:
python test_admin_scope.py \
  --admin-cpf 11122233344 --admin-password "senha_admin" \
  --user-cpf 99988877766 --user-password "senha_user"
"""

import argparse
import json
import sys
from typing import Dict, Tuple

import requests


def login_with_cpf(base_url: str, cpf: str, password: str) -> Tuple[requests.Session, Dict]:
    session = requests.Session()
    url = f"{base_url.rstrip('/')}/api/login/cpf/secure/"
    response = session.post(url, json={"cpf": cpf, "password": password}, timeout=15)

    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text}

    if response.status_code != 200:
        raise RuntimeError(
            f"Falha no login CPF={cpf}. Status={response.status_code}. Resposta={data}"
        )

    token = data.get("access_token")
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})

    return session, data


def hit(session: requests.Session, method: str, url: str, **kwargs) -> Tuple[int, Dict]:
    response = session.request(method=method, url=url, timeout=15, **kwargs)
    try:
        payload = response.json()
    except Exception:
        payload = {"raw": response.text}
    return response.status_code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Teste de escopo ADM")
    parser.add_argument("--base-url", default="http://localhost:8000", help="URL base do backend")
    parser.add_argument("--admin-cpf", required=True, help="CPF do usuário administrador")
    parser.add_argument("--admin-password", required=True, help="Senha do usuário administrador")
    parser.add_argument("--user-cpf", required=True, help="CPF do usuário comum")
    parser.add_argument("--user-password", required=True, help="Senha do usuário comum")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    print("=" * 72)
    print("TESTE DE ESCOPO ADMINISTRATIVO (ADM x USER)")
    print("=" * 72)

    print("\n[1/4] Logando como usuário comum...")
    user_session, user_info = login_with_cpf(base, args.user_cpf, args.user_password)
    print(f"  ✓ Login usuário comum OK | user_id={user_info.get('user', {}).get('id')}")

    print("\n[2/4] Logando como administrador...")
    admin_session, admin_info = login_with_cpf(base, args.admin_cpf, args.admin_password)
    print(f"  ✓ Login admin OK | user_id={admin_info.get('user', {}).get('id')}")

    tests = [
        {
            "name": "Listar usuários (admin only)",
            "method": "GET",
            "path": "/api/list/usuarios/",
            "expected_user": {401, 403},
            "expected_admin": {200},
            "kwargs": {},
        },
        {
            "name": "Config email admin (admin only)",
            "method": "GET",
            "path": "/api/admin/email-config/",
            "expected_user": {401, 403},
            "expected_admin": {200},
            "kwargs": {},
        },
        {
            "name": "Delete usuário por CPF (manual is_staff)",
            "method": "DELETE",
            "path": "/api/delete/usuario/?cpf=00000000000",
            "expected_user": {401, 403},
            "expected_admin": {200, 404},
            "kwargs": {},
        },
    ]

    failures = []
    print("\n[3/4] Validando escopo em endpoints sensíveis...")

    for idx, item in enumerate(tests, start=1):
        url = f"{base}{item['path']}"

        user_status, user_payload = hit(user_session, item["method"], url, **item["kwargs"])
        admin_status, admin_payload = hit(admin_session, item["method"], url, **item["kwargs"])

        user_ok = user_status in item["expected_user"]
        admin_ok = admin_status in item["expected_admin"]
        test_ok = user_ok and admin_ok

        marker = "PASS" if test_ok else "FAIL"
        print(f"  [{idx}] {marker} - {item['name']}")
        print(f"      user={user_status} (esperado {sorted(item['expected_user'])})")
        print(f"      admin={admin_status} (esperado {sorted(item['expected_admin'])})")

        if not test_ok:
            failures.append(
                {
                    "test": item["name"],
                    "user_status": user_status,
                    "admin_status": admin_status,
                    "user_body": user_payload,
                    "admin_body": admin_payload,
                }
            )

    print("\n[4/4] Resultado final")
    if failures:
        print("  ❌ FALHA: há endpoints com escopo incorreto")
        print(json.dumps(failures, indent=2, ensure_ascii=False))
        return 1

    print("  ✅ SUCESSO: escopo ADM validado nos endpoints testados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
