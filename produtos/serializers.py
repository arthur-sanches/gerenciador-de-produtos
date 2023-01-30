from rest_framework import serializers

from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('nome', 'sku', 'preco', 'descricao', 'datahora_adicionado', 'datahora_modificado')
        model = Produto