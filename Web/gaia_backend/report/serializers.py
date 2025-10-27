from rest_framework import serializers
from .models import Propriedade, Laudo

class PropriedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propriedade
        fields = '__all__'  # Pega todos os campos do model

class LaudoSerializer(serializers.ModelSerializer):
    # Campos extras que não estão no model, mas são úteis para o frontend
    propriedade_nome = serializers.CharField(source='propriedade.nome', read_only=True)
    arquivo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Laudo
        fields = [
            'id',
            'numero_amostra', 
            'data_coleta',
            'arquivo_pdf',
            'arquivo_url',           # Campo extra
            'propriedade_nome',      # Campo extra
            'propriedade'            # ID da propriedade
        ]
    
    def get_arquivo_url(self, obj):
        """Gera a URL completa para baixar o PDF"""
        if obj.arquivo_pdf:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.arquivo_pdf.url)
        return None