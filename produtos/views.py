from decimal import Decimal

from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response

import pandas

from .models import Produto
from .serializers import ProdutoSerializer, CSVUploadSerializer


def _trata_preco(preco):
        return Decimal(preco.replace(',', '.'))


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
                        preco= _trata_preco(row['preco']),
                        descricao= row["descricao"]
                        )
                new_file.save()
            except Exception as e:
                print(e)
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class ProdutoExportCSV(generics.ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self, requisicao):
        queryset = Produto.objects.all()
        nome_param = self.request.query_params.get('nome')
        sku_param = self.request.query_params.get('sku')
        preco_param = self.request.query_params.get('preco')
        preco_maior_param = self.request.query_params.get('preco_maior')
        preco_menor_param = self.request.query_params.get('preco_menor')
        if nome_param is not None:
            queryset = queryset.filter(nome=nome_param)
        if sku_param is not None:
            queryset = queryset.filter(sku=sku_param)
        if preco_param is not None:
            queryset = queryset.filter(preco=_trata_preco(preco_param))
        if preco_maior_param is not None:
            queryset = queryset.filter(preco__gte=Decimal(_trata_preco(preco_maior_param)))
        if preco_menor_param is not None:
            queryset = queryset.filter(preco__lte=Decimal(_trata_preco(preco_menor_param)))
        return queryset

    def get(self, requisicao):
        produtos_csv = []
        for produto in self.get_queryset(requisicao):
            produtos_csv.append({'nome': produto.nome, 'sku': produto.sku, 'preco': produto.preco, 
            'descricao': produto.descricao})
        resultados = pandas.DataFrame(produtos_csv)

        resposta = HttpResponse(content_type='text/csv')
        resposta['Content-Disposition'] = 'attachment; filename=export.csv'

        resultados.to_csv(path_or_buf=resposta,sep=';',float_format='%.2f',index=False,decimal=",")
        return resposta
        
