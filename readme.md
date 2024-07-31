# DJANGO SEND IMAGE REGISTER

    - API consumida por requisições HTTP vindo do flutter, recebendo dados, de uma fazenda, uma pessoa e uma foto associada, e salvando-as no banco de dados. Pode cadastrar os dados de Pessoas, Fazendas e Fotos e listar quais Pessoas e Fazendas estão cadastradas no banco. Salva a imagem na api `media/photos` e consequentemente no banco de dados

### Autor
    - Roberto Pereira de Freitas Neto

## Requerimentos
    - Anaconda 
    - Django 5.0+
    - Django Rest Framework 3.0+
    - PostgreSQL 16+
    - Psycopg2 2.9.9

## Setup inicial

1. Clone o repositório

2. Siga o passo a passo para criar o ambiente virtual Anaconda:
```
    conda create --name (nome_do_ambiente)
    conda activate (nome_do_ambiente)

    pip install django
    pip install djangorestframework
    pip install psycopg2

    conda deactivate 
    conda activate (nome_do_ambiente)
```

3. Instalar PostgreSQL seguindo as instrucoes [no site do programa](https://www.postgresql.org/download/) e configurar ela com base na [secao acima sobre configurando a database](#setup-da-database-postgresql).

    2.1 - Criação do DATABASE (Se preferir, pode usar o PgAdmin4 como alternativa)

    ```
    sudo -u postgres psql
    CREATE ROLE database_user LOGIN PASSWORD senha CREATEDB
    exit

    psql template1 -U database_user
    CREATE DATABASE image_upload OWNER database_user
    exit

    got to /etc/postgresql/<version>/main/pg_hba.conf :
    sudo nano pg_hba.conf
    mudar as seguintes linhas a seguir:
    // local" is for Unix domain socket connections only
    local all all md5

    restart the database
    sudo systemctl restart postgresqlf
    ```
    as chaves secretas estão na seção #keys abaixo

4. Configure as variáveis de ambiente:
```
    conda env config vars set SECRET_KEY='(chave secreta do django)'

    conda env config vars set DB_DJANGO_USER='(nome do usuário do banco de dados)'

    conda env config vars set DB_DJANGO_PASSWORD='(senha do banco de dados)'

    conda env config vars set DB_DJANGO_NAME='(nome do banco de dados)'

    conda env config vars set IP_MACHINE'(ip da sua máquina)'

    conda deactivate 
    conda activate (nome_do_ambiente)
```
## Setup Django

- Após a instalação de todos os requimentos, criação e configuração do banco de dados 


```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py run server (ip_da_maquina):8000
``` 


## Keys

Por questões de segurança, solicitar a secret_key para o administrador.

## Sobre o recebimento de fotos

 - Apenas uma imagem por vez
 - todas as fotos serão salvas na pasta `/media/photos`