from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, ConfiguracaoEmail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        cpf = data.get('cpf')
        password = data.get('password')

        if cpf and password:
            # Remove formatação do CPF (pontos e traços)
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            # Tenta autenticar por CPF
            user = authenticate(username=cpf_limpo, password=password)
            
            if not user:
                raise serializers.ValidationError('Credenciais inválidas')
            
            data['user'] = user
        else:
            raise serializers.ValidationError('CPF e senha são obrigatórios')

        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado que estende TokenObtainPairSerializer
    e adiciona o campo 'primeiro_acesso' e informações do usuário
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Adiciona informações do usuário e campo primeiro_acesso
        user = self.user
        data['user'] = {
            'id': user.id,
            'nome': f'{user.first_name} {user.last_name}'.strip(),
            'email': user.email,
            'cpf': user.cpf,
            'is_staff': user.is_staff,
            'primeiro_acesso': user.primeiro_acesso,
        }
        
        return data

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'cpf')

class ConfiguracaoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoEmail
        fields = ('id', 'assunto', 'mensagem', 'updated_at')