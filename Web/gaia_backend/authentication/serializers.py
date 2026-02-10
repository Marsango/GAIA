from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, ConfiguracaoEmail

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

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'cpf')

class ConfiguracaoEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoEmail
        fields = ['id', 'assunto', 'mensagem', 'updated_at']