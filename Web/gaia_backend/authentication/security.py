"""
Módulo de segurança progressiva com rate limiting e CAPTCHA
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache
import secrets
import string
from .models import LoginAttempt, CaptchaChallenge
from django.contrib.auth import get_user_model

User = get_user_model()

# ===============================================
# 🔐 RATE LIMITING PROGRESSIVO
# ===============================================

def record_login_attempt(identifier, ip_address, success=False):
    """Registra uma tentativa de login"""
    LoginAttempt.objects.create(
        identifier=identifier,
        ip_address=ip_address,
        success=success
    )


def get_failed_attempts(identifier, ip_address, minutes=60):
    """Retorna o número de falhas nos últimos N minutos"""
    cutoff = timezone.now() - timedelta(minutes=minutes)
    return LoginAttempt.objects.filter(
        identifier=identifier,
        ip_address=ip_address,
        success=False,
        timestamp__gte=cutoff
    ).count()


def get_login_security_status(identifier, ip_address):
    """
    Retorna o status de segurança do login (rate limit progressivo):
    
    - 0-2 falhas: Sem restrição ✅
    - 3-4 falhas: Aguardar 30 segundos entre tentativas ⚠️
    - 5+ falhas: Requer CAPTCHA 🚫
    """
    failed = get_failed_attempts(identifier, ip_address, minutes=60)
    
    return {
        'failed_attempts': failed,
        'require_wait': failed >= 3,
        'require_captcha': failed >= 5,
        'wait_seconds': 30 if failed >= 3 else 0,
    }


def should_block_login(identifier, ip_address):
    """Verifica se deve bloquear completamente (após múltiplas tentativas)"""
    failed = get_failed_attempts(identifier, ip_address, minutes=60)
    return failed >= 10  # Bloqueio total após 10 falhas


# ===============================================
# 🤖 CAPTCHA MATEMÁTICO SIMPLES
# ===============================================

CAPTCHA_OPERATIONS = [
    (lambda a, b: a + b, "{} + {} = ?"),
    (lambda a, b: a - b, "{} - {} = ?"),
    (lambda a, b: a * b, "{} × {} = ?"),
]


def generate_captcha():
    """Gera um desafio CAPTCHA matemático simples"""
    import random
    
    # Selecionar operação aleatória
    operation, template = random.choice(CAPTCHA_OPERATIONS)
    
    # Gerar números aleatórios (1-20)
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    
    # Calcular resposta correta
    correct_answer = str(operation(a, b))
    challenge_key = template.format(a, b)
    
    return challenge_key, correct_answer


def create_captcha_challenge(identifier, ip_address):
    """Cria um novo desafio CAPTCHA para o usuário"""
    # Remover CAPTCHAs expirados/antigos
    CaptchaChallenge.objects.filter(
        identifier=identifier,
        ip_address=ip_address
    ).delete()
    
    # Gerar novo desafio
    challenge_key, correct_answer = generate_captcha()
    token = secrets.token_urlsafe(32)
    
    expires_at = timezone.now() + timedelta(minutes=10)  # Válido por 10 minutos
    
    captcha = CaptchaChallenge.objects.create(
        identifier=identifier,
        ip_address=ip_address,
        challenge_token=token,
        challenge_key=challenge_key,
        correct_answer=correct_answer,
        expires_at=expires_at
    )
    
    return {
        'token': token,
        'challenge': challenge_key,
        'expires_in_seconds': 600  # 10 minutos
    }


def verify_captcha(token, user_answer):
    """Verifica a resposta do CAPTCHA"""
    try:
        captcha = CaptchaChallenge.objects.get(challenge_token=token)
        
        # Verificar se expirou
        if timezone.now() > captcha.expires_at:
            captcha.delete()
            return False, "CAPTCHA expirou"
        
        # Verificar se já foi resolvido
        if captcha.is_solved:
            return False, "CAPTCHA já foi resolvido"
        
        # Incrementar tentativas
        captcha.attempts += 1
        
        # Bloquear após 5 tentativas incorretas
        if captcha.attempts >= 5:
            captcha.delete()
            return False, "Muitas tentativas. CAPTCHA bloqueado"
        
        # Comparar resposta
        if str(user_answer).strip() == captcha.correct_answer:
            captcha.is_solved = True
            captcha.save()
            return True, "CAPTCHA resolvido com sucesso"
        else:
            captcha.save()
            remaining = 5 - captcha.attempts
            return False, f"Resposta incorreta ({remaining} tentativas restantes)"
    
    except CaptchaChallenge.DoesNotExist:
        return False, "Token de CAPTCHA inválido ou expirado"


def clear_failed_attempts(identifier, ip_address):
    """Limpa as tentativas falhadas após login bem-sucedido"""
    LoginAttempt.objects.filter(
        identifier=identifier,
        ip_address=ip_address,
        success=False
    ).delete()
