# 🧠 ToT - Text Of Things

Este projeto é uma aplicação Flask com integração à AWS simulada via LocalStack. Ele permite o upload de imagens via API, armazenamento no S3 e envio de mensagens para processamento assíncrono via SQS. Um worker consome essas mensagens, processa as imagens com OpenCV e salva os resultados em outro bucket.

---

## 📦 Estrutura do Projeto

```
tot-project/
├── app/
│   ├── api/
│   │   └── main.py               # API Flask com Swagger
│   ├── utils/
│   │   └── aws_helpers.py        # Funções auxiliares (S3, SQS, processamento)
│   └── worker/
│       └── worker.py             # Worker para processar imagens da fila
├── docker/
│   ├── bootstrap_localstack.sh   # Script de criação dos recursos no LocalStack
│   └── entrypoint.sh             # (opcional) Script de inicialização
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── send_image_message.py         # Script auxiliar para envio de mensagens
├── teste.png                     # Imagem de teste (opcional)
└── README.md
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/tot-project.git
cd tot-project
```

### 2. Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Subir o LocalStack e a API Flask
```bash
docker-compose up --build
```

### 5. Criar recursos no LocalStack
Em outro terminal:
```bash
bash docker/bootstrap_localstack.sh
```

---

## 📡 Endpoints

Acesse a documentação Swagger em:  
http://localhost:5000/

| Método | Rota              | Descrição                          |
|--------|-------------------|-------------------------------------|
| GET    | `/healthcheck`    | Verifica se a API está online       |
| GET    | `/process`        | Verifica se o worker está rodando   |
| POST   | `/images/upload`  | Envia uma imagem PNG via multipart  |

---

## 🧵 Executar o Worker

```bash
python -m app.worker.worker
```

⚠️ Deve ser executado a partir da raiz do projeto.

---

## 🧪 Testar envio manual de mensagem

```bash
python send_image_message.py
```

---

## 📚 Variáveis de Ambiente

| Variável       | Valor padrão     |
|----------------|------------------|
| AWS_ACCESS_KEY | test             |
| AWS_SECRET_KEY | test             |
| REGION         | us-east-1        |
| ENDPOINT_URL   | http://localhost:4566 |

---

## 🔍 Exemplo de Requisição via `curl`

```bash
curl -X POST http://localhost:5000/images/upload \
  -F "image=@teste.png"
```

---

## 🧼 Dicas de Estilo

- Código e comentários em inglês
- Logs legíveis e informativos
- Separação de responsabilidades (API vs Worker vs Utils)

---

## 📸 Exemplo de Log Esperado

```bash
✅ Bucket found: image-input
✅ Queue is ready: new-image-input.fifo
🔁 Worker started. Listening for messages...
📦 Message received: teste.png
✅ Processed and uploaded to image-processed
```

---

## 🛠️ Tecnologias

- Python 3.9+
- Flask + Flask-RESTX
- Boto3
- OpenCV
- LocalStack (S3 + SQS)
- Docker / Docker Compose

---

## 📌 Créditos

Projeto desenvolvido para fins educacionais, com foco em processamento assíncrono de imagens utilizando arquitetura desacoplada com filas e armazenamento em nuvem simulado.