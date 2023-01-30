import json

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Produto
from .serializers import ProdutoSerializer


class ProdutoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        produto1 = Produto.objects.create(
            nome='Camiseta Lorem Ipsum', 
            sku='LO123RES45IPSUM', 
            preco=99.90, 
            descricao="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin. In eget orci malesuada, 
                        porta lacus non, cursus justo. Quisque ornare lorem nec aliquam scelerisque. 
                        Aliquam erat volutpat. Nulla ac tristique lectus, at rutrum tortor. In 
                        molestie aliquet risus, sed fermentum nulla pulvinar ut. Curabitur vel 
                        lobortis nunc. Duis tempus consequat ipsum vel sollicitudin. In hac 
                        habitasse platea dictumst. Aliquam tempus felis vitae malesuada volutpat. 
                        Nunc ultricies augue et libero lobortis tincidunt.""",
        )

    def test_info_produto(self):
        produto = Produto.objects.get(id=1)
        nome = f'{produto.nome}'
        sku = f'{produto.sku}'
        preco = f'{produto.preco}'
        descricao = f'{produto.descricao}'
        self.assertEqual(nome, 'Camiseta Lorem Ipsum')
        self.assertEqual(sku, 'LO123RES45IPSUM')
        self.assertEqual(preco, '99.90')
        self.assertEqual(descricao, """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin. In eget orci malesuada, 
                        porta lacus non, cursus justo. Quisque ornare lorem nec aliquam scelerisque. 
                        Aliquam erat volutpat. Nulla ac tristique lectus, at rutrum tortor. In 
                        molestie aliquet risus, sed fermentum nulla pulvinar ut. Curabitur vel 
                        lobortis nunc. Duis tempus consequat ipsum vel sollicitudin. In hac 
                        habitasse platea dictumst. Aliquam tempus felis vitae malesuada volutpat. 
                        Nunc ultricies augue et libero lobortis tincidunt.""")


class ProdutoAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Produto.objects.create(
            nome='Camiseta Lorem Ipsum', 
            sku='LO123RES45IPSUM', 
            preco=99.90, 
            descricao="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin. In eget orci malesuada, 
                        porta lacus non, cursus justo. Quisque ornare lorem nec aliquam scelerisque. 
                        Aliquam erat volutpat. Nulla ac tristique lectus, at rutrum tortor. In 
                        molestie aliquet risus, sed fermentum nulla pulvinar ut. Curabitur vel 
                        lobortis nunc. Duis tempus consequat ipsum vel sollicitudin. In hac 
                        habitasse platea dictumst. Aliquam tempus felis vitae malesuada volutpat. 
                        Nunc ultricies augue et libero lobortis tincidunt.""",
        )
        Produto.objects.create(
            nome='Boné Lorem Ipsum', 
            sku='LO678RES99IPSUM', 
            preco=49.90, 
            descricao="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",
        )

    def test_api_produto(self):
        resposta = self.client.get('/api/1/')
        self.assertEqual(resposta.data, {'nome': 'Camiseta Lorem Ipsum', 'sku': 'LO123RES45IPSUM', 
                        'preco': '99.90', 'descricao': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin. In eget orci malesuada, 
                        porta lacus non, cursus justo. Quisque ornare lorem nec aliquam scelerisque. 
                        Aliquam erat volutpat. Nulla ac tristique lectus, at rutrum tortor. In 
                        molestie aliquet risus, sed fermentum nulla pulvinar ut. Curabitur vel 
                        lobortis nunc. Duis tempus consequat ipsum vel sollicitudin. In hac 
                        habitasse platea dictumst. Aliquam tempus felis vitae malesuada volutpat. 
                        Nunc ultricies augue et libero lobortis tincidunt."""})

    def test_api_lista_produtos(self):
        resposta = self.client.get('/api/')
        self.assertEqual(resposta.data, [{'nome': 'Camiseta Lorem Ipsum', 'sku': 'LO123RES45IPSUM', 
                        'preco': '99.90', 'descricao': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin. In eget orci malesuada, 
                        porta lacus non, cursus justo. Quisque ornare lorem nec aliquam scelerisque. 
                        Aliquam erat volutpat. Nulla ac tristique lectus, at rutrum tortor. In 
                        molestie aliquet risus, sed fermentum nulla pulvinar ut. Curabitur vel 
                        lobortis nunc. Duis tempus consequat ipsum vel sollicitudin. In hac 
                        habitasse platea dictumst. Aliquam tempus felis vitae malesuada volutpat. 
                        Nunc ultricies augue et libero lobortis tincidunt."""}, 
                        {'nome': 'Boné Lorem Ipsum', 'sku': 'LO678RES99IPSUM', 
                        'preco': '49.90', 'descricao': """Lorem ipsum dolor sit amet, consectetur adipiscing elit."""}])

    def test_api_adiciona_produto(self):
        produto = {'nome': 'Tênis Lorem Ipsum', 'sku': 'LO555RES55IPSUM', 
                        'preco': '199.90', 'descricao': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Curabitur commodo sit amet nulla eget sollicitudin."""}
        resposta = self.client.post('/api/', produto, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 3)
    
    def test_api_modifica_produto(self):
        url = '/api/2/'
        produto = {'nome': 'Boné Lorem Ipsum', 'sku': 'LO678RES99IPSUM', 
                        'preco': '79.90', 'descricao': """Boné Lorem Ipsum dolor sit amet, consectetur adipiscing elit."""}
        resposta = self.client.put(url, produto, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        resposta_get = self.client.get(url)
        self.assertEqual(resposta_get.data, produto)

    def test_api_deleta_produto(self):
        resposta = self.client.delete('/api/2/')
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
