from rest_framework import serializers
from .models import Propriedade, Laudo, Amostra, Empresa, Person, Endereco

class AmostraSerializer(serializers.ModelSerializer):
    
    propriedade_name = serializers.CharField(source='propriedade.name', read_only=True)
    propriedade_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Amostra
        fields = '__all__'
        read_only_fields = ['usuario', 'data_cadastro']
    
    def create(self, validated_data):
        # O campo usuario sera preenchido automaticamente pelo save() do modelo
        # Nao atribuimos o request.user aqui pois ele eh um Usuario, nao uma Person
        return super().create(validated_data)
    
    def to_internal_value(self, data):
        # Mapear propriedade_id para propriedade se fornecido
        if 'propriedade_id' in data and 'propriedade' not in data:
            data['propriedade'] = data.pop('propriedade_id')
        return super().to_internal_value(data)


class LaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = '__all__'
    
    def get_arquivo_url(self, obj):
        """Gera a URL completa para baixar o PDF"""
        if obj.arquivo_pdf:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.arquivo_pdf.url)
        return None
    
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
    
    def validate_cpf(self, value):
        """Valida CPF único no modelo Person (report)"""
        # Remover formatação
        cpf_limpo = ''.join(filter(str.isdigit, str(value)))
        
        # Verificar se já existe (exceto se for atualização)
        instance = self.instance
        if instance:
            # Atualização - verificar se mudou
            if Person.objects.filter(cpf=cpf_limpo).exclude(id=instance.id).exists():
                raise serializers.ValidationError(
                    f'CPF {value} já está cadastrado para outra pessoa.'
                )
        else:
            # Criação - verificar se já existe
            if Person.objects.filter(cpf=cpf_limpo).exists():
                raise serializers.ValidationError(
                    f'CPF {value} já está cadastrado.'
                )
        
        return cpf_limpo

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class PropriedadeSerializer(serializers.ModelSerializer):
    proprietario_id = serializers.IntegerField(write_only=True, required=True, 
                                               error_messages={
                                                   'required': 'Propriedade DEVE ter um proprietário (pessoa ou empresa)!',
                                                   'null': 'Proprietário não pode ser nulo!'
                                               })
    endereco_detalhes = EnderecoSerializer(source='endereco', read_only=True)
    

    class Meta:
        model = Propriedade
        fields = '__all__'

    def create(self, validated_data):
        print(f"DEBUG PropriedadeSerializer.create: {validated_data}")
        
        proprietario_id = validated_data.pop('proprietario_id', None)
        
        # VALIDAÇÃO CRÍTICA: proprietario_id é OBRIGATÓRIO
        if not proprietario_id:
            raise serializers.ValidationError({
                'proprietario_id': 'ERRO CRÍTICO: Propriedade não pode ser criada sem proprietário!'
            })

        # tenta pessoa
        pessoa = Person.objects.filter(id=proprietario_id).first()
        if pessoa:
            print(f"   ✅ Proprietário encontrado: Person ID {pessoa.id} - {pessoa.name}")
            validated_data['proprietario_pessoa'] = pessoa
            return super().create(validated_data)

        # tenta empresa
        empresa = Empresa.objects.filter(id=proprietario_id).first()
        if empresa:
            print(f"   ✅ Proprietário encontrado: Empresa ID {empresa.id} - {empresa.name}")
            validated_data['proprietario_empresa'] = empresa
            return super().create(validated_data)

        # NENHUM proprietário encontrado - ERRO CRÍTICO
        raise serializers.ValidationError({
            'proprietario_id': f'Proprietário com ID {proprietario_id} não encontrado. '
                              f'Verifique se pessoa/empresa existe no sistema.'
        })
