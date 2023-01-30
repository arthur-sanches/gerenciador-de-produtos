# imagem base
FROM python:3.8

# configura variavel de ambiente
ENV DockerHOME=/home/app/webapp

# cria diretorio
RUN mkdir -p $DockerHOME

# define diretorio de trabalho
WORKDIR $DockerHOME

# define algumas variaveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# instala dependencias pip
RUN pip install --upgrade pip

# copia o projeto para o diretorio home do docker
COPY . $DockerHOME

# instala todas as dependencias do projeto
RUN pip install -r requirements.txt

# expoe a porta 8000 que sera usada pela aplicacao
EXPOSE 8000

# inicia o servidor da aplicao
CMD python manage.py runserver