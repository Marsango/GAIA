from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UsuarioSerializer

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite acesso sem login
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)  # Cria a sessão
        
        user_data = UsuarioSerializer(user).data
        return Response({
            'message': 'Login realizado com sucesso',
            'user': user_data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout realizado com sucesso'})

@api_view(['GET'])
def user_info(request):
    """Retorna informações do usuário logado"""
    user = request.user
    if user.is_authenticated:
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)
    return Response({'error': 'Usuário não autenticado'}, status=401)