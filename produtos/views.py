from decimal import Decimal

from rest_framework import generics, status
from rest_framework.response import Response

import pandas

from .models import Produto
from .serializers import ProdutoSerializer, CSVUploadSerializer


class ProdutoList(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class ProdutoImportCSV(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = CSVUploadSerializer

    def post(self, requisicao, *args, **kwargs):
        serializer = self.get_serializer(data=requisicao.data)
        serializer.is_valid(raise_exception=True)
        csv = serializer.validated_data['csv']
        reader = pandas.read_csv(csv)
        for label, row in reader.iterrows():
            try:
                new_file = Produto(
                        nome = row['nome'],
                        sku= row["sku"],
                        preco= self._trata_preco(row['preco']),
                        descricao= row["descricao"]
                        )
                new_file.save()
            except Exception as e:
                print(e)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)

    def _trata_preco(self, preco):
        return Decimal(preco.replace(',', '.'))


class ProdutoExportCSV(generics.RetrieveAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
