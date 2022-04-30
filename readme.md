# Sistema de Irrigação Autônoma de Planta usando Raspberry Pi 4 - API

API projeto final de conclusão de curso ADS-IFBA

## Conteúdo

- [Pré-requisitos](#pré-requisitos)
- [Execução Aplicação](#execução)


## Pré-requisitos

Estas são as instalações e configurações necessárias para executar o projeto.

Para executar este projeto é necessário instalar:

- Python 3

1. Após a instalação

   - Execute o seguinte comando no terminal 

         python -version

    - Resultado esperado

            Python 3.7.0

## Execução

1. Clonar repositório git utilizando o comando:

        git clone git@github.com:elayneargollo/tcc-back.git

2. Vá ate a pasta do projeto

        cd app/main

3. Criar ambiente virtual 

        python -m venv virtual-env

4. Ative seu ambiente virtual

        source virtual-env/bin/activate

5. Install all dependencies

        pip install -r requirements.txt
        
6. Criar arquivo de configuração na raiz do main

   - Crie um arquivo chamado de secrets.json com os valores das variáveis sensíveis

         {
             "JWT_SECRET_KEY": "DontTellAnyone",
             "JWT_BLACKLIST_ENABLED": "True",
             "MAILGUN_DOMAIN": {sandbox},
             "MAILGUN_API_KEY": {key_sandbox},
             "API_URL": {path_swagger},
             "SWAGGER_URL":"/swagger"
         }
        
7. Execute o programa

         python app.py
         
Após a execução a inicialização conseguirá acessar:

   - Raiz da API: http://localhost:5000
   - Documentação no Swagger :  http://localhost:5000/swagger/

### Autora

<img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/48841005?s=40&v=4" width="100px;" alt=""/>
 
Feito por Elayne Natália 👋🏽 

[![Linkedin Badge](https://img.shields.io/badge/-Elayne-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/elayne/)](https://www.linkedin.com/in/elayne-nat%C3%A1lia/) 

