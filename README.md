# Gerenciador de Produtos para Ecommerce

### Descrição

Esse projeto tem por objetivo demonstrar uma API para Ecommerce, que receba produtos através de um 
arquivo csv com 4 colunas, sendo elas: nome, sku, preço e descrição. Além de exportar produtos, com 
filtros ou sem, para um arquivo csv.
Também é possível criar, ler, modificar e deletar produtos através de requisições HTTP.


### Instruções

- clone o projeto
- abra um terminal dentro da pasta do projeto
- instale os requisitos do projeto no terminal usando um dos dois comandos a seguir: 
    - (recomendado) "pipenv install -r requirements.txt"
    - "pip install -r requirements.txt"
- se você usou o passo recomendado anteriormente (pipenv) use o seguinte comando para iniciar o env:
    - "pipenv shell"
- inicie o servidor django com o comando:
    - "python manage.py runserver"
- o serviço está pronto para testes através da url:
    - localhost:8000/api/
- para parar o servidor pressione 'Ctrl + C' no terminal
- e então digite 'exit' caso esteja dentro de um env (pipenv):


### Endpoints

- 'api/'            : Lista todos os produtos cadastrados.

- 'api/{id}/'       : Entra no detalhe de um determinado produto usando seu id de cadastro.

- 'api/import-csv/' : Permite o upload de um arquivo csv para inserção massiva de produtos.
    Dentro da pasta do projeto existe um arquivo chamado 'exemplo.csv' com 20 produtos para 
    exemplificar o formato e o tipo dos dados que podem ser importados pela aplicação através de 
    um arquivo csv.

- 'api/export-csv/' : Gera um arquivo csv com os produtos filtrados de acordo com alguns parâmetros.
    - Parâmetros para filtras produtos ao gerar csv:
        - nome
        - sku
        - preco
    - Exemplos de url com parâmetros:
        - "api/export-csv/?sku=LO123REM45IPS"
            Exporta arquivo csv com somente um produto com sku igual a LO123REM45IPS.
        - "api/export-csv/?preco=99.90"
            Exporta arquivo csv com somente produtos com preço igual a 99.90.


### Características dos campos dos produtos:
- nome = CharField(max_length=80)
- sku = CharField(max_length=64, unique=True)
- preco = DecimalField(max_digits=7, decimal_places=2)
- descricao = TextField(default='')


### Exemplo de dados de produtos:

|    nome    |      sku      |    preco    |    descricao                                          |
|------------|---------------|-------------|-------------------------------------------------------|
| Boné       | LO123REM45IPS |    29.90    |Lorem ipsum dolor sit amet, consectetur adipiscing elit|    
| Saia       | LO523REM46IPS |    39.90    |Lorem ipsum dolor sit amet, consectetur adipiscing elit|    
| Calça      | LO333REM33IPS |    99.90    |Lorem ipsum dolor sit amet, consectetur adipiscing elit|    
| Camiseta   | LO444REM44IPS |    26.90    |Lorem ipsum dolor sit amet, consectetur adipiscing elit|    
