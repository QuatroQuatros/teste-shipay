# teste-shipay

## Descrição

API Flask para o teste da shipay

## Pré-requisitos

Antes de executar a aplicação, certifique-se de ter as seguintes dependências instaladas:

Se for rodar sem utilizar containers:
- Python (versão 3.9.0)
- pip (gerenciador de pacotes do Python)
- python virtual Environment (venv)
- mysql (5.7 ou superior)

Se for rodar utilizando containers:
- Docker 
- Docker compose

## Instalação

1. Clone o repositório do projeto:

   ```bash
   git clone https://github.com/seu-usuario/minha-aplicacao-flask.git`
   ```
2. Vá até o diretório da aplicação
   cd teste-shipay/api

3. Instale o virtual env caso ainda não possua
   ```bash
   python3 -m pip install --user virtualenv
   ```
4. Crie um novo ambiente virtual para isolar as dependências:
   ```bash
   python3 -m venv worspace
   ```
5. Ative seu ambiente virtual:
- No windows:
  ```bash
   venv\Scripts\activate
  ```
- No Linux ou Mac:
  ```bash
   source venv/bin/activate
  ```
6. Instale as dependências do projeto:

  ```bash
   pip3 install -r requirements.txt
  ```

7. Crie o arquivo .env:
  ```bash
   cp .env-example .env
  ```
8. Configure seu .env

9. Inicie a aplicação:
  ```bash
   python3 ./main.py
  ```
