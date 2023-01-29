from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):
    nome = models.CharField(max_length=80)
    sku = models.CharField(max_length=64, unique=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    descricao = models.TextField(default='')
    datahora_adicionado = models.DateTimeField(auto_now_add=True)
    datahora_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
