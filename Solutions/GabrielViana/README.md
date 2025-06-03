## 📋 Pré-requisitos

Para rodar este projeto você precisa ter instalado:
* Docker
* Docker Compose


## 🚀 Começando

Estas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 🔧 Instalação e Execução

1. Clone o repositório
```bash
git clone Gabriellavoura/material-apoio-tot
cd material-apoio-tot/Solutions/GabrielViana
```

2. Construa e inicie os containers
```bash
docker-compose up --build
```

Este comando irá:
- Iniciar o LocalStack (simulando AWS S3 e SQS)
- Construir a imagem Docker da aplicação
- Iniciar o container da API
- Expor a API na porta 5000

### 📦 Comandos Docker Compose Disponíveis

O projeto utiliza Docker Compose para orquestração:

* `docker compose up --build`: Constrói e executa todos os serviços
* `docker compose up -d`: Executa em background
* `docker compose down`: Para e remove os containers
* `docker compose logs -f`: Visualiza os logs em tempo real
* `docker compose exec app bash`: Acessa o terminal do container da aplicação


## 🔎 Endpoints da API

A API possui os seguintes endpoints principais:

### Upload de Imagens
- `POST /upload/`: Upload de imagens PNG para processamento
  - Parâmetros: `file` (multipart/form-data)
  - Resposta: ID único da imagem e status do upload

### Health Check
- `GET /health/`: Verifica o status da aplicação e dependências
  - Resposta: Status dos serviços S3 e SQS

### Status de Processamento
- `GET /process/`: Verifica o status do worker de processamento
  - Resposta: Status atual do worker

### Documentação Interativa
- `GET /docs/`: Documentação Swagger/OpenAPI interativa


### Portas

- **API Flask**: 5000
- **LocalStack**: 4566


## 🔄 Fluxo de Processamento

1. **Upload**: Imagem PNG é enviada via POST para `/upload/`
2. **Armazenamento**: Imagem é salva no bucket S3 `image-input`
3. **Fila**: Mensagem é enviada para a fila SQS `new-image-input.fifo`
4. **Processamento**: Worker consome mensagens da fila e processa imagens
5. **Resultado**: Imagem processada é salva no bucket S3 `image-processed`



### Logs

Para visualizar os logs em tempo real:

```bash
docker compose logs -f flask-app
```




