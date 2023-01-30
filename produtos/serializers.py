from rest_framework import serializers

from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('nome', 'sku', 'preco', 'descricao')
        model = Produto


class CSVUploadSerializer(serializers.Serializer):
    csv = serializers.FileField()
