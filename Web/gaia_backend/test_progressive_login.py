#!/usr/bin/env python
"""
Teste automatizado do fluxo de login progressivo com CAPTCHA.

Fluxo validado:
1) Envia tentativas inválidas até o backend exigir CAPTCHA
2) Resolve o CAPTCHA matemático retornado pela API
3) Tenta autenticar com CAPTCHA resolvido

Uso:
  python test_progressive_login.py --cpf 12345678900 --wrong-password senha_errada
  python test_progressive_login.py --cpf 12345678900 --wrong-password senha_errada --correct-password MinhaSenha123
"""

import argparse
import re
import sys
import time
from typing import Optional, Tuple

import requests


def solve_math_challenge(challenge: str) -> Optional[int]:
    """Resolve expressões simples no formato 'A + B = ?'."""
    normalized = challenge.replace("×", "*").replace("x", "*").replace("X", "*")
    match = re.search(r"(-?\d+)\s*([+\-*])\s*(-?\d+)", normalized)
    if not match:
        return None

    left = int(match.group(1))
    operator = match.group(2)
    right = int(match.group(3))

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    return None


def post_login(url: str, payload: dict) -> Tuple[int, dict]:
    response = requests.post(url, json=payload, timeout=10)
    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text}
    return response.status_code, data


def run_test(base_url: str, cpf: str, wrong_password: str, correct_password: Optional[str]) -> int:
    endpoint = f"{base_url.rstrip('/')}/api/login/cpf/secure/"
    print(f"\nEndpoint: {endpoint}")
    print(f"CPF: {cpf}")

    captcha = None
    max_attempts = 8

    print("\n[1/3] Forçando falhas até exigir CAPTCHA...")
    for attempt in range(1, max_attempts + 1):
        status_code, data = post_login(
            endpoint,
            {
                "cpf": cpf,
                "password": wrong_password,
            },
        )

        require_captcha = bool(data.get("require_captcha"))
        print(
            f"Tentativa {attempt}: status={status_code} "
            f"failed_attempts={data.get('failed_attempts')} require_captcha={require_captcha}"
        )

        if require_captcha and isinstance(data.get("captcha"), dict):
            captcha = data["captcha"]
            break

        time.sleep(0.15)

    if not captcha:
        print("\n❌ CAPTCHA não foi exigido dentro do número esperado de tentativas.")
        print("Verifique se você está chamando /api/login/cpf/secure/ e se as migrations foram aplicadas.")
        return 1

    challenge = captcha.get("challenge") or captcha.get("challenge_key")
    token = captcha.get("challenge_token") or captcha.get("token") or captcha.get("challenge_key")

    if not challenge or not token:
        print("\n❌ Resposta de CAPTCHA incompleta:")
        print(captcha)
        return 1

    answer = solve_math_challenge(challenge)
    if answer is None:
        print(f"\n❌ Não consegui resolver automaticamente o desafio: {challenge}")
        return 1

    print("\n[2/3] Validando envio de CAPTCHA com senha inválida...")
    status_code, data = post_login(
        endpoint,
        {
            "cpf": cpf,
            "password": wrong_password,
            "captcha_token": token,
            "captcha_answer": str(answer),
        },
    )
    print(f"Status: {status_code} | Resposta: {data}")

    if status_code not in (401, 403):
        print("⚠️ Resposta inesperada no passo de CAPTCHA + senha inválida.")

    if not correct_password:
        print("\n✅ Teste parcial concluído: fluxo de CAPTCHA foi acionado e submetido.")
        print("Dica: passe --correct-password para validar login completo após CAPTCHA.")
        return 0

    next_captcha = data.get("captcha") if isinstance(data, dict) else None
    if isinstance(next_captcha, dict):
        challenge = next_captcha.get("challenge") or next_captcha.get("challenge_key") or challenge
        token = (
            next_captcha.get("challenge_token")
            or next_captcha.get("token")
            or next_captcha.get("challenge_key")
            or token
        )
        solved = solve_math_challenge(challenge)
        if solved is not None:
            answer = solved

    print("\n[3/3] Tentando login correto com CAPTCHA...")
    status_code, data = post_login(
        endpoint,
        {
            "cpf": cpf,
            "password": correct_password,
            "captcha_token": token,
            "captcha_answer": str(answer),
        },
    )

    print(f"Status final: {status_code}")
    print(f"Resposta final: {data}")

    if status_code == 200 and isinstance(data, dict) and data.get("user"):
        print("\n✅ Teste completo OK: login com CAPTCHA funcionou.")
        return 0

    print("\n❌ Login final não retornou sucesso (200).")
    print("Confirme CPF/senha corretos e se o frontend envia captcha_token + captcha_answer.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Teste do login progressivo com CAPTCHA")
    parser.add_argument("--base-url", default="http://localhost:8000", help="URL base do backend")
    parser.add_argument("--cpf", required=True, help="CPF de teste")
    parser.add_argument("--wrong-password", default="senha_errada", help="Senha inválida para forçar bloqueio")
    parser.add_argument(
        "--correct-password",
        default=None,
        help="Senha correta para validar login completo após CAPTCHA",
    )
    args = parser.parse_args()

    return run_test(
        base_url=args.base_url,
        cpf=args.cpf,
        wrong_password=args.wrong_password,
        correct_password=args.correct_password,
    )


if __name__ == "__main__":
    sys.exit(main())
