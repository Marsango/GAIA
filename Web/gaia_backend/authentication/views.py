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
                    'last_name': user.last_name
                    })