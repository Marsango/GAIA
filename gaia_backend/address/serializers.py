# gaia_backend/address/serializers.py

from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__' # Isso diz para o serializer incluir todos os campos do modelo