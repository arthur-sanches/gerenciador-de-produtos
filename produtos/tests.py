from django.test import TestCase
from django.contrib.auth.models import User

from .models import Produto


class ProdutoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        produto = Produto.objects.create(
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
