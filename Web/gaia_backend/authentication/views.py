from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .serializers import LoginSerializer, UsuarioSerializer
from .models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string

from .models import Usuario, ConfiguracaoEmail
from .serializers import LoginSerializer, UsuarioSerializer, ConfiguracaoEmailSerializer

from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
@permission_classes([AllowAny])
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
                return Response({'error': 'Conta desativada'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Senha incorreta'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({'error': 'CPF não cadastrado'}, status=status.HTTP_404_NOT_FOUND)
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


# 2. Troca de Senha (Primeiro Acesso ou Manual)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Permite ao usuário logado alterar sua senha.
    Remove a flag de 'primeiro_acesso'.
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not new_password:
        return Response({'error': 'Nova senha é obrigatória.'}, status=status.HTTP_400_BAD_REQUEST)

    # Verifica a senha antiga (se fornecida, é uma boa prática)
    if old_password and not user.check_password(old_password):
        return Response({'error': 'Senha antiga incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.primeiro_acesso = False
    user.save()

    return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)


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
def sync_usuario(request):
    """API simples para o software cadastrar usuários"""
    try:
        data = request.data
        
        # Verifica se usuário já existe
        cpf = data.get('cpf')
        if Usuario.objects.filter(cpf=cpf).exists():
            return Response({
                'status': 'exists',
                'message': 'Usuário já existe'
            }, status=status.HTTP_200_OK)
        
        # Cria novo usuário
        usuario = Usuario.objects.create(
            username=cpf,  # Usa CPF como username
            cpf=cpf,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', f'{cpf}@temp.com'),
            telefone=data.get('telefone', ''),
            password=make_password(data.get('password', '123456'))
        )
        
        return Response({
            'id': usuario.id,
            'status': 'created',
            'message': 'Usuário criado com sucesso'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Retorna informações do usuário logado"""
    user = request.user
    
    return Response({'id': user.id,
                    'nome': f"{user.first_name} {user.last_name}",
                    'cpf': user.cpf,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff
                    })