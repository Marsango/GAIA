from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .serializers import LoginSerializer, UsuarioSerializer, CustomTokenObtainPairSerializer
from .models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django_ratelimit.decorators import ratelimit

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario, ConfiguracaoEmail
from .serializers import LoginSerializer, UsuarioSerializer, ConfiguracaoEmailSerializer, CustomTokenObtainPairSerializer

from rest_framework.permissions import IsAdminUser

# ============ NOVO: View customizada que retorna primeiro_acesso ============
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada que estende TokenObtainPairView
    e usa CustomTokenObtainPairSerializer para incluir
    informações do usuário e campo primeiro_acesso
    """
    serializer_class = CustomTokenObtainPairSerializer
# ==========================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='20/m', method='POST', block=True)
def login_with_cpf(request):
    """Login usando CPF (para site e software)"""
    cpf = request.data.get('cpf')
    password = request.data.get('password')
    
    if not cpf or not password:
        return Response(
            {'error': 'CPF e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    User = get_user_model()
    
    try:
        # Buscar usuário por CPF
        if hasattr(User(), 'cpf'):
            user = User.objects.get(cpf=cpf)
        else:
            cpf_limpo = cpf.replace('.', '').replace('-', '')
            user = User.objects.get(username=cpf_limpo)
        
        # Verificar senha
        if user.check_password(password):
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'nome': f'{user.first_name} {user.last_name}'.strip(),
                        'email': user.email,
                        'cpf': cpf,
                        'is_staff': user.is_staff,
                        # AQUI ESTÁ A ATUALIZAÇÃO IMPORTANTE:
                        'primeiro_acesso': user.primeiro_acesso,
                    }
                })
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='20/m', method='POST', block=True)
def login_with_cnpj(request):
    """Login usando CNPJ (para empresas)"""
    cnpj = request.data.get('cnpj')
    password = request.data.get('password')
    
    if not cnpj or not password:
        return Response(
            {'error': 'CNPJ e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    User = get_user_model()
    
    try:
        # Buscar usuário por CNPJ
        cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
        user = User.objects.get(cnpj=cnpj_limpo)
        
        # Verificar senha
        if user.check_password(password):
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'nome': f'{user.first_name} {user.last_name}'.strip(),
                        'email': user.email,
                        'cnpj': cnpj_limpo,
                        'is_staff': user.is_staff,
                        'primeiro_acesso': user.primeiro_acesso,
                    }
                })
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 1. Cadastro de Cliente com Envio de Senha
@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_client_email(request):
    """
    Cadastra o usuário, gera uma senha aleatória e envia por e-mail.
    """
    data = request.data
    email = data.get('email')
    cpf = data.get('cpf')
    nome = data.get('first_name')

    if not email or not cpf:
        return Response({'error': 'Email e CPF são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    if Usuario.objects.filter(cpf=cpf).exists():
        return Response({'error': 'CPF já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Usuario.objects.filter(email=email).exists():
        return Response({'error': 'Email já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Gera uma senha aleatória
        temp_password = get_random_string(length=12)

        # Cria o usuário
        user = Usuario.objects.create(
            username=cpf, # Mantemos CPF como username interno
            cpf=cpf,
            email=email,
            first_name=nome,
            last_name=data.get('last_name', ''),
            primeiro_acesso=True # Marca para trocar a senha depois
        )
        user.set_password(temp_password)
        user.save()
        # Senha gerada com sucesso (não registrar em logs por segurança)

        # 1. Pega o template do banco (ou cria se não existir)
        config_email, _ = ConfiguracaoEmail.objects.get_or_create(id=1)
        
        assunto_email = config_email.assunto
        mensagem_template = config_email.mensagem

        # 2. Substitui os placeholders ({nome}, {senha}) pelos dados reais
        # Usamos .format() de forma segura. Se o ADM apagou a tag {senha}, o Python não quebra, mas a senha não vai.
        try:
            mensagem_final = mensagem_template.format(
                nome=nome,
                cpf=cpf,
                senha=temp_password,
                email=email
            )
        except KeyError:
            # Fallback: Se o ADM bagunçou as tags (ex: colocou {telefone} que não existe),
            # voltamos para um texto simples para garantir o envio.
            mensagem_final = f"Olá {nome}, sua senha temporária é: {temp_password}"

        # 3. Envia
        send_mail(
            assunto_email,
            mensagem_final,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'admin@gaia.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Usuário criado e e-mail enviado.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Cadastro de Empresa com Envio de Senha
@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_company_email(request):
    """
    Cadastra uma empresa, gera uma senha aleatória e envia por e-mail.
    """
    print("\n" + "="*60)
    print("🏢 REGISTER_COMPANY_EMAIL - Iniciando registro de empresa")
    print("="*60)
    
    data = request.data
    email = data.get('email')
    cnpj = data.get('cnpj')
    nome = data.get('first_name')

    print(f"📮 Email: {email}")
    print(f"🏢 CNPJ: {cnpj}")
    print(f"📝 Nome: {nome}")

    if not email or not cnpj:
        print("❌ Email ou CNPJ não fornecidos")
        return Response({'error': 'Email e CNPJ são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    # Limpar CNPJ
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
    print(f"✅ CNPJ limpo: {cnpj_limpo}")

    if Usuario.objects.filter(cnpj=cnpj_limpo).exists():
        print("❌ CNPJ já cadastrado")
        return Response({'error': 'CNPJ já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Usuario.objects.filter(email=email).exists():
        print("❌ Email já cadastrado")
        return Response({'error': 'Email já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Gera uma senha aleatória
        temp_password = get_random_string(length=12)
        # Senha gerada com sucesso (não registrar em logs por segurança)

        # Cria o usuário com CNPJ
        user = Usuario.objects.create(
            username=cnpj_limpo,  # CNPJ como username interno
            cnpj=cnpj_limpo,
            email=email,
            first_name=nome,
            last_name=data.get('last_name', ''),
            primeiro_acesso=True  # Marca para trocar a senha depois
        )
        user.set_password(temp_password)
        user.save()
        print(f"✅ Usuário criado: ID={user.id}")

        # 1. Pega o template do banco (ou cria se não existir)
        config_email, _ = ConfiguracaoEmail.objects.get_or_create(id=1)
        
        assunto_email = config_email.assunto
        mensagem_template = config_email.mensagem
        print(f"📧 Assunto: {assunto_email}")

        # 2. Substitui os placeholders pelos dados reais
        # Template pode ter {cpf} ou {cnpj}, então passamos ambos
        try:
            mensagem_final = mensagem_template.format(
                nome=nome,
                cpf=cnpj_limpo,  # Compatibilidade: se template usar {cpf}, recebe o CNPJ
                cnpj=cnpj_limpo,  # Se template usar {cnpj}, também funciona
                senha=temp_password,
                email=email
            )
        except KeyError as e:
            # Fallback: template com placeholder desconhecido
            print(f"⚠️ Placeholder desconhecido no template: {e}")
            mensagem_final = f"""Olá {nome},

Seu cadastro no sistema GAIA foi realizado com sucesso.

Suas credenciais de acesso são:
Login (CNPJ): {cnpj_limpo}
Senha Temporária: {temp_password}

Por favor, altere sua senha no primeiro acesso."""
        
        print(f"📝 Mensagem preparada, tamanho: {len(mensagem_final)} caracteres")

        # 3. Envia
        print(f"📤 Enviando email para: {email}")
        print(f"   Backend: {settings.EMAIL_BACKEND}")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        
        num_sent = send_mail(
            assunto_email,
            mensagem_final,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'admin@gaia.com',
            [email],
            fail_silently=False,
        )
        
        print(f"✅ Email enviado! Emails enviados: {num_sent}")
        print("="*60 + "\n")

        return Response({'message': 'Empresa cadastrada e e-mail enviado.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"❌ ERRO ao registrar empresa: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*60 + "\n")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Permite ao usuário logado alterar sua senha.
    Remove a flag de 'primeiro_acesso'.
    """
    try:
        user = request.user
        
        print(f"\n[change_password] Tentativa de mudança de senha")
        print(f"  Usuário autenticado: {user.is_authenticated}")
        print(f"  ID do usuário: {user.id if hasattr(user, 'id') else 'N/A'}")
        print(f"  CPF do usuário: {user.cpf if hasattr(user, 'cpf') else 'N/A'}")
        
        if not user.is_authenticated:
            print(f"  ❌ Usuário não autenticado!")
            return Response({'error': 'Usuário não autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        print(f"  Senha antiga fornecida: {'sim' if old_password else 'não'}")
        print(f"  Senha nova fornecida: {'sim' if new_password else 'não'}")

        if not new_password:
            return Response({'error': 'Nova senha é obrigatória.'}, status=status.HTTP_400_BAD_REQUEST)

        if not old_password:
            return Response({'error': 'Senha atual é obrigatória.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar força da nova senha
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            # Formatar mensagens de validação de senha para serem mais específicas
            error_messages = []
            
            for message in e.messages:
                message_str = str(message)
                
                # Traduzir e melhorar mensagens específicas do Django
                if 'too short' in message_str.lower() or 'must contain at least' in message_str.lower():
                    error_messages.append('❌ Senha muito curta - deve ter pelo menos 8 caracteres')
                elif 'entirely numeric' in message_str.lower():
                    error_messages.append('❌ Senha não pode conter apenas números')
                elif 'too similar' in message_str.lower():
                    error_messages.append('❌ Senha é muito similar ao nome de usuário ou email')
                elif 'common password' in message_str.lower():
                    error_messages.append('❌ Senha é muito comum - escolha uma senha mais segura (ex: MinhaSe9ha!)')
                else:
                    # Se não for mensagem conhecida, incluir a mensagem original
                    error_messages.append(f'❌ {message_str}')
            
            return Response({
                'error': 'Senha fraca - não atende aos requisitos de segurança',
                'motivos': error_messages,
                'requisitos': [
                    'Mínimo 8 caracteres',
                    'Não pode ser apenas números',
                    'Não pode ser similar ao nome de usuário',
                    'Não pode ser uma senha comum (ex: 12345678, password)'
                ]
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verifica a senha antiga
        print(f"  Testando check_password...")
        print(f"    Senha fornecida tem {len(old_password)} caracteres")
        print(f"    Primeiro caractere: '{old_password[0] if old_password else 'vazia'}'")
        print(f"    Último caractere: '{old_password[-1] if old_password else 'vazia'}'")
        
        is_password_correct = user.check_password(old_password)
        print(f"    Resultado check_password: {is_password_correct}")
        
        if not is_password_correct:
            print(f"  ❌ Senha atual incorreta!")
            return Response({'error': 'Senha atual incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"  ✅ Senha atual verificada com sucesso!")
        user.set_password(new_password)
        user.primeiro_acesso = False
        user.save()

        print(f"  ✅ Senha alterada e primeiro_acesso definido como False")
        return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"  ❌ ERRO INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'Erro ao processar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3. Esqueci Minha Senha (Reset Simples enviando nova senha)
# Nota: Para um fluxo mais seguro em produção, usa-se links com tokens, 
# mas este método envia uma nova senha provisória direto para simplificar o MVP.
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    
    try:
        user = Usuario.objects.get(email=email)
        
        new_password = get_random_string(length=12)
        user.set_password(new_password)
        user.primeiro_acesso = True # Força trocar de novo
        user.save()

        subject = 'Recuperação de Senha - GAIA'
        message = f"""
        Olá {user.first_name},

        Você solicitou a recuperação de senha.
        Sua nova senha temporária é: {new_password}

        Use-a para logar e defina uma nova senha imediatamente.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'admin@gaia.com',
            [email],
            fail_silently=False,
        )
        
        return Response({'message': 'Uma nova senha foi enviada para seu e-mail.'}, status=status.HTTP_200_OK)

    except Usuario.DoesNotExist:
        # Por segurança, não dizemos explicitamente que o email não existe, ou dizemos genericamente
        return Response({'message': 'Se o e-mail estiver cadastrado, você receberá uma nova senha.'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser]) # Só ADM pode mexer aqui
def manage_email_template(request):
    """
    GET: Retorna o template atual.
    POST: Atualiza o template.
    """
    # Tenta pegar a configuração existente, se não existir, cria uma padrão
    config, created = ConfiguracaoEmail.objects.get_or_create(id=1)

    if request.method == 'GET':
        serializer = ConfiguracaoEmailSerializer(config)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConfiguracaoEmailSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Template de e-mail atualizado com sucesso!', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "nome": f"{user.first_name} {user.last_name}",
                "cpf": user.cpf,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    return Response({'message': 'Logout realizado com sucesso'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_usuario(request):
    """API simples para o software cadastrar usuários - Requer autenticação"""
    print(f"\n📝 [sync_usuario] Solicitação recebida")
    print(f"   Usuário logado: {request.user.username} (is_staff: {request.user.is_staff})")
    print(f"   Dados: {request.data}")
    
    try:
        # Verificar se o usuário logado é admin
        if not request.user.is_staff:
            print(f"❌ Usuário não é admin!")
            return Response(
                {'error': 'Apenas administradores podem cadastrar usuários'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data
        
        # Validar CPF (obrigatório)
        cpf = data.get('cpf', '').strip()
        if not cpf:
            print(f"❌ CPF não fornecido")
            return Response(
                {'error': 'CPF é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar email (obrigatório e único)
        email = data.get('email', '').strip()
        if not email:
            print(f"❌ Email não fornecido")
            return Response(
                {'error': 'Email é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar formato básico de email
        if '@' not in email or '.' not in email:
            print(f"❌ Email inválido: {email}")
            return Response(
                {'error': f'Email "{email}" é inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se CPF já existe
        if Usuario.objects.filter(cpf=cpf).exists():
            user = Usuario.objects.get(cpf=cpf)
            user_id = user.id
            print(f"⚠️  CPF já existe com ID: {user_id} (is_staff: {user.is_staff})")
            return Response({
                'error': f"CPF {cpf} já está cadastrado no sistema (ID: {user_id})",
                'status': 'cpf_exists',
                'id': user_id,
            }, status=status.HTTP_409_CONFLICT)
        
        # Verificar se email já existe
        if Usuario.objects.filter(email=email).exists():
            existing_user = Usuario.objects.get(email=email)
            print(f"⚠️  Email já existe com ID: {existing_user.id}")
            return Response({
                'error': f'Email "{email}" já está cadastrado. Use outro email!',
                'status': 'email_exists',
                'id': existing_user.id,
            }, status=status.HTTP_409_CONFLICT)
        
        # Cria novo usuário
        first_name = data.get('first_name', '').strip()
        if not first_name:
            print(f"❌ Nome é obrigatório")
            return Response(
                {'error': 'Nome é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        print(f"   Validações OK. Criando novo usuário...")
        print(f"   - CPF: {cpf}")
        print(f"   - Email: {email}")
        print(f"   - Nome: {first_name}")
        
        usuario = Usuario.objects.create(
            username=cpf,  # Usa CPF como username
            cpf=cpf,
            first_name=first_name,
            last_name=data.get('last_name', '').strip(),
            email=email,  # Email único
            telefone=data.get('phone_number', '').strip(),
            password=make_password(data.get('password', '123456'))
        )
        
        print(f"✅ Usuário criado com sucesso! ID: {usuario.id}")
        return Response({
            'id': usuario.id,
            'status': 'created',
            'message': 'Usuário criado com sucesso',
            'cpf': usuario.cpf,
            'email': usuario.email,
            'name': usuario.first_name
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_usuarios(request):
    """Lista todos os usuários cadastrados via sync_usuario"""
    print(f"\n📋 [list_usuarios] Solicitação recebida")
    print(f"   Usuário logado: {request.user.username}")
    
    try:
        # Filtros opcionais
        cpf_filter = request.query_params.get('cpf')
        name_filter = request.query_params.get('name')
        
        usuarios = Usuario.objects.all()
        
        # Aplicar filtros
        if cpf_filter:
            usuarios = usuarios.filter(cpf__icontains=cpf_filter)
        if name_filter:
            usuarios = usuarios.filter(first_name__icontains=name_filter)
        
        # Ordenar por ID descendente (mais recentes primeiro)
        usuarios = usuarios.order_by('-id')
        
        # Serializar
        data = []
        for user in usuarios:
            data.append({
                'id': user.id,
                'username': user.username,
                'name': f"{user.first_name} {user.last_name}".strip(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'cpf': user.cpf,
                'email': user.email,
                'telefone': getattr(user, 'telefone', ''),
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'data_criacao': user.date_joined.isoformat() if hasattr(user, 'date_joined') else None,
            })
        
        print(f"✅ {len(data)} usuário(s) encontrado(s)")
        return Response({
            'count': len(data),
            'results': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_usuario(request):
    """Exclui um usuario pelo CPF (apenas admins)."""
    if not request.user.is_staff:
        return Response(
            {'error': 'Apenas administradores podem excluir usuários'},
            status=status.HTTP_403_FORBIDDEN
        )

    cpf = request.query_params.get('cpf') or request.data.get('cpf')
    if not cpf:
        return Response({'error': 'CPF é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Usuario.objects.get(cpf=cpf)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({'message': 'Usuário excluído com sucesso.'}, status=status.HTTP_200_OK)

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Retorna informações do usuário logado, incluindo primeiro_acesso"""
    user = request.user
    
    return Response({'id': user.id,
                    'nome': f"{user.first_name} {user.last_name}",
                    'cpf': user.cpf,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'primeiro_acesso': user.primeiro_acesso
                    })


# ENDPOINT DE TESTE PARA ENVIO DE EMAIL
@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_send_email(request):
    """
    Endpoint de teste para verificar se o envio de email está funcionando
    POST /api/test-email/
    Body: {"email": "seu_email@gmail.com"}
    """
    print("\n" + "="*60)
    print("📧 TEST_SEND_EMAIL - Enviando email de teste")
    print("="*60)
    
    email = request.data.get('email')
    if not email:
        print("❌ Email não fornecido")
        return Response({'error': 'Email é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        print(f"📮 Email de destino: {email}")
        print(f"📧 Backend configurado: {settings.EMAIL_BACKEND}")
        print(f"📨 Remetente (FROM): {settings.DEFAULT_FROM_EMAIL}")
        print(f"🏠 Host SMTP: {settings.EMAIL_HOST}")
        print(f"🔌 Porta: {settings.EMAIL_PORT}")
        print(f"🔐 TLS: {settings.EMAIL_USE_TLS}")
        
        assunto = "GAIA - Email de Teste"
        mensagem = """
Olá!

Este é um email de teste do sistema GAIA.

Se você recebeu este email, significa que o sistema de envio de emails está funcionando corretamente!

---
Sistema GAIA
Laboratório de Solos - UTFPR
"""
        
        print(f"\n📝 Enviando email...")
        num_sent = send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        print(f"✅ Email enviado com sucesso! Emails enviados: {num_sent}")
        print("="*60 + "\n")
        
        return Response({'message': f'Email enviado com sucesso para {email}'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"❌ ERRO ao enviar email: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*60 + "\n")
        return Response({'error': f'Erro ao enviar email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========== SINCRONIZAÇÃO DE DADOS EMPRESA/PERSON ↔ USUARIO ==========

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def sync_usuario_by_cpf(request):
    """
    Sincroniza dados do Usuario quando Person é editada
    PATCH /api/sync/usuario/cpf/
    Body: {
        "cpf": "12345678900",
        "email": "novo@email.com",
        "first_name": "Nome Novo",
        "telefone": "11987654321"
    }
    """
    print(f"\n🔵 sync_usuario_by_cpf CHAMADO", flush=True)
    print(f"   Request data: {request.data}", flush=True)
    
    cpf = request.data.get('cpf')
    
    if not cpf:
        print(f"❌ CPF não fornecido", flush=True)
        return Response({'error': 'CPF é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Normalizar CPF
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    print(f"   CPF normalizado: {cpf_limpo}", flush=True)
    
    try:
        usuario = Usuario.objects.get(cpf=cpf_limpo)
        print(f"✅ Usuario encontrado: ID={usuario.id}, username={usuario.username}", flush=True)
        
        # Atualizar campos fornecidos
        alteracoes = []
        
        # Se forneceu NEW_CPF, atualizar o CPF do Usuario também
        if 'new_cpf' in request.data and request.data['new_cpf']:
            new_cpf = request.data['new_cpf'].replace('.', '').replace('-', '')
            print(f"   🔄 Atualizando CPF: '{usuario.cpf}' → '{new_cpf}'", flush=True)
            usuario.cpf = new_cpf
            # Atualizar username também (se for baseado em CPF)
            if usuario.username and usuario.username.replace('.', '').replace('-', '') == cpf_limpo:
                print(f"   🔄 Atualizando username: '{usuario.username}' → '{new_cpf}'", flush=True)
                usuario.username = new_cpf
            alteracoes.append(f"cpf")
        
        if 'email' in request.data:
            print(f"   Atualizando email: '{usuario.email}' → '{request.data['email']}'", flush=True)
            usuario.email = request.data['email']
            alteracoes.append(f"email")
        if 'first_name' in request.data:
            print(f"   Atualizando first_name: '{usuario.first_name}' → '{request.data['first_name']}'", flush=True)
            usuario.first_name = request.data['first_name']
            alteracoes.append(f"first_name")
        if 'telefone' in request.data:
            print(f"   Atualizando telefone: '{usuario.telefone}' → '{request.data['telefone']}'", flush=True)
            usuario.telefone = request.data['telefone']
            alteracoes.append(f"telefone")
        
        if not alteracoes:
            print(f"⚠️ Nenhum campo foi enviado para atualizar", flush=True)
            return Response({'warning': 'Nenhum campo para atualizar'}, status=status.HTTP_200_OK)
        
        usuario.save()
        print(f"💾 Usuario salvo com sucesso", flush=True)
        print(f"✅ Campos atualizados: {', '.join(alteracoes)}", flush=True)
        
        return Response({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'telefone': usuario.telefone,
            'updated_fields': alteracoes
        }, status=status.HTTP_200_OK)
        
    except Usuario.DoesNotExist:
        print(f"❌ Usuario com CPF {cpf_limpo} NÃO ENCONTRADO", flush=True)
        return Response(
            {'error': f'Usuario com CPF {cpf_limpo} não encontrado no banco'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"❌ Erro ao sincronizar Usuario (CPF): {e}", flush=True)
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def sync_usuario_by_cnpj(request):
    """
    Sincroniza dados do Usuario quando Empresa é editada
    PATCH /api/sync/usuario/cnpj/
    Body: {
        "cnpj": "12345678000190",
        "email": "novo@empresa.com",
        "first_name": "Nome Empresa Novo",
        "telefone": "1133334444"
    }
    """
    print(f"\n🔵 sync_usuario_by_cnpj CHAMADO", flush=True)
    print(f"   Request data: {request.data}", flush=True)
    
    cnpj = request.data.get('cnpj')
    
    if not cnpj:
        print(f"❌ CNPJ não fornecido", flush=True)
        return Response({'error': 'CNPJ é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Normalizar CNPJ
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
    print(f"   CNPJ normalizado: {cnpj_limpo}", flush=True)
    
    try:
        usuario = Usuario.objects.get(cnpj=cnpj_limpo)
        print(f"✅ Usuario encontrado: ID={usuario.id}, username={usuario.username}", flush=True)
        
        # Atualizar campos fornecidos
        alteracoes = []
        
        # Se forneceu NEW_CNPJ, atualizar o CNPJ do Usuario também
        if 'new_cnpj' in request.data and request.data['new_cnpj']:
            new_cnpj = request.data['new_cnpj'].replace('.', '').replace('/', '').replace('-', '')
            print(f"   🔄 Atualizando CNPJ: '{usuario.cnpj}' → '{new_cnpj}'", flush=True)
            usuario.cnpj = new_cnpj
            # Atualizar username também (se for baseado em CNPJ)
            if usuario.username and usuario.username.replace('.', '').replace('/', '').replace('-', '') == cnpj_limpo:
                print(f"   🔄 Atualizando username: '{usuario.username}' → '{new_cnpj}'", flush=True)
                usuario.username = new_cnpj
            alteracoes.append(f"cnpj")
        
        if 'email' in request.data:
            print(f"   Atualizando email: '{usuario.email}' → '{request.data['email']}'", flush=True)
            usuario.email = request.data['email']
            alteracoes.append(f"email")
        if 'first_name' in request.data:
            print(f"   Atualizando first_name: '{usuario.first_name}' → '{request.data['first_name']}'", flush=True)
            usuario.first_name = request.data['first_name']
            alteracoes.append(f"first_name")
        if 'telefone' in request.data:
            print(f"   Atualizando telefone: '{usuario.telefone}' → '{request.data['telefone']}'", flush=True)
            usuario.telefone = request.data['telefone']
            alteracoes.append(f"telefone")
        
        if not alteracoes:
            print(f"⚠️ Nenhum campo foi enviado para atualizar", flush=True)
            return Response({'warning': 'Nenhum campo para atualizar'}, status=status.HTTP_200_OK)
        
        usuario.save()
        print(f"💾 Usuario salvo com sucesso", flush=True)
        print(f"✅ Campos atualizados: {', '.join(alteracoes)}", flush=True)
        
        return Response({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'telefone': usuario.telefone,
            'updated_fields': alteracoes
        }, status=status.HTTP_200_OK)
        
    except Usuario.DoesNotExist:
        print(f"❌ Usuario com CNPJ {cnpj_limpo} NÃO ENCONTRADO", flush=True)
        return Response(
            {'error': f'Usuario com CNPJ {cnpj_limpo} não encontrado no banco'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"❌ Erro ao sincronizar Usuario (CNPJ): {e}", flush=True)
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_usuario_by_cpf(request):
    """
    Deleta Usuario por CPF (usado internamente quando Person é excluída)
    DELETE /api/delete/usuario/cpf/
    Params: cpf=12345678900
    """
    print(f"\n🔵 delete_usuario_by_cpf CHAMADO", flush=True)
    
    cpf = request.query_params.get('cpf') or request.data.get('cpf')
    
    if not cpf:
        print(f"❌ CPF não fornecido", flush=True)
        return Response({'error': 'CPF é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Normalizar CPF
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    print(f"   CPF normalizado: {cpf_limpo}", flush=True)
    
    try:
        usuario = Usuario.objects.get(cpf=cpf_limpo)
        print(f"✅ Usuario encontrado: ID={usuario.id}, username={usuario.username}, cpf={cpf_limpo}", flush=True)
        
        usuario_id = usuario.id
        usuario.delete()
        print(f"💾 Usuario ID {usuario_id} deletado com sucesso", flush=True)
        
        return Response({
            'message': f'Usuario com CPF {cpf_limpo} deletado com sucesso',
            'id': usuario_id
        }, status=status.HTTP_200_OK)
        
    except Usuario.DoesNotExist:
        print(f"❌ Usuario com CPF {cpf_limpo} NÃO ENCONTRADO", flush=True)
        return Response(
            {'warning': f'Usuario com CPF {cpf_limpo} não encontrado no banco'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"❌ Erro ao deletar Usuario (CPF): {e}", flush=True)
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_usuario_by_cnpj(request):
    """
    Deleta Usuario por CNPJ (usado internamente quando Empresa é excluída)
    DELETE /api/delete/usuario/cnpj/
    Params: cnpj=12345678000190
    """
    print(f"\n🔵 delete_usuario_by_cnpj CHAMADO", flush=True)
    
    cnpj = request.query_params.get('cnpj') or request.data.get('cnpj')
    
    if not cnpj:
        print(f"❌ CNPJ não fornecido", flush=True)
        return Response({'error': 'CNPJ é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Normalizar CNPJ
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
    print(f"   CNPJ normalizado: {cnpj_limpo}", flush=True)
    
    try:
        usuario = Usuario.objects.get(cnpj=cnpj_limpo)
        print(f"✅ Usuario encontrado: ID={usuario.id}, username={usuario.username}, cnpj={cnpj_limpo}", flush=True)
        
        usuario_id = usuario.id
        usuario.delete()
        print(f"💾 Usuario ID {usuario_id} deletado com sucesso", flush=True)
        
        return Response({
            'message': f'Usuario com CNPJ {cnpj_limpo} deletado com sucesso',
            'id': usuario_id
        }, status=status.HTTP_200_OK)
        
    except Usuario.DoesNotExist:
        print(f"❌ Usuario com CNPJ {cnpj_limpo} NÃO ENCONTRADO", flush=True)
        return Response(
            {'warning': f'Usuario com CNPJ {cnpj_limpo} não encontrado no banco'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"❌ Erro ao deletar Usuario (CNPJ): {e}", flush=True)
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)