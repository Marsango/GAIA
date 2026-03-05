"""
Middleware de segurança para adicionar headers HTTP de proteção
"""


class SecurityHeadersMiddleware:
    """
    Adiciona headers de segurança essenciais a todas as respostas HTTP
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # X-Content-Type-Options: Previne MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options: Já configurado pelo Django, mas garantindo
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'
        
        # Referrer-Policy: Controla informações de referer
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy: Desabilita APIs perigosas
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content-Security-Policy: Proteção contra XSS e injeção de código
        # Nota: Ajustar conforme necessidade da aplicação
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",  # unsafe-inline necessário para React
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
        ]
        response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        return response


class JWTCookieToHeaderMiddleware:
    """
    Middleware que lê o access_token do httpOnly cookie
    e o injeta no Authorization header para validação pelo Django
    
    Isso permite que o backend valide tokens via cookies,
    mantendo a segurança de httpOnly (inacessível via JavaScript)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Se não há Authorization header, tenta ler do cookie
        if 'HTTP_AUTHORIZATION' not in request.META:
            access_token = request.COOKIES.get('access_token')
            
            if access_token:
                # Injetar no Authorization header para validação
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                print(f'[JWT] 🔄 Token injetado do cookie para header (len={len(access_token)})')
        
        response = self.get_response(request)
        return response
