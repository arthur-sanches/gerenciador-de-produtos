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

def _preco_eh_positivo(preco):
    return True if preco > 0.00 else False


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
        descricao_param = self.request.query_params.get('descricao')
        
        queryset = self.filtro_nome(queryset, nome_param)
        queryset = self.filtro_sku(queryset, sku_param)
        queryset = self.filtro_preco(queryset, preco_param)
        queryset = self.filtro_preco_maior(queryset, preco_maior_param)
        queryset = self.filtro_preco_menor(queryset, preco_menor_param)
        queryset = self.filtro_descricao(queryset, descricao_param)

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

    def _valida_preco(self, preco):
        if preco is not None:
            preco_tratado = Decimal(_trata_preco(preco))
            if _preco_eh_positivo(preco_tratado):
                return preco_tratado
        return False

    def filtro_nome(self, queryset, nome_param):
        if nome_param is not None:
            return queryset.filter(nome__contains=nome_param)
        return queryset
    
    def filtro_sku(self, queryset, sku_param):
        if sku_param is not None:
            return queryset.filter(sku=sku_param)
        return queryset
    
    def filtro_preco(self, queryset, preco_param):
        preco_validado = self._valida_preco(preco_param)
        if preco_validado:
            return queryset.filter(preco=preco_validado)
        return queryset
    
    def filtro_preco_maior(self, queryset, preco_maior_param):
        preco_validado = self._valida_preco(preco_maior_param)
        if preco_validado:
            return queryset.filter(preco__gte=preco_validado)
        return queryset
    
    def filtro_preco_menor(self, queryset, preco_menor_param):
        preco_validado = self._valida_preco(preco_menor_param)
        if preco_validado:
            return queryset.filter(preco__lte=preco_validado)
        return queryset

    def filtro_descricao(self, queryset, descricao_param):
        if descricao_param is not None:
            return queryset.filter(descricao__contains=descricao_param)
        return queryset
