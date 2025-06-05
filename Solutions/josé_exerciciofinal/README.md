# 🖼️ Image Processor - OCR

Pipeline completo de processamento de imagens usando Flask + OpenCV + AWS (S3/SQS via LocalStack) totalmente dockerizado.

Este sistema permite:

- 📤 Upload de imagens `.png` para um bucket S3 (`image-input`)
- 📩 Envio de notificação para a fila SQS (`new-image-input.fifo`)
- ⚙️ Worker que faz polling da fila, processa a imagem (binarização com OpenCV)
- 📥 Salva o resultado no bucket S3 (`image-processed`)
- 🔔 Envia mensagem para a fila `new-image-processed.fifo`
- 🌐 Visualiza imagens processadas em uma interface web

---

##  Diagrama da Aplicação

```plaintext
Usuário ⇄ API Flask ⇄ S3 (image-input)
                  ⇓
             SQS (new-image-input.fifo)
                  ⇓
              Worker Flask ⇄ S3 (image-processed)
                  ⇓
             SQS (new-image-processed.fifo)
```

---

##  Como executar localmente

### ✅ Pré-requisitos

- Docker
- Docker Compose

### ▶️ Subir os containers

```bash
docker-compose up --build
```

Isso irá:

- Subir o LocalStack (emulando AWSLOCAL)
- Criar buckets e filas automaticamente
- Subir a API Flask na porta `5000`

---

## ⚙️ Funcionalidades

###  Healthcheck

```http
GET /image/healthcheck
```

**Resposta:**

```json
{"status": "ok"}
```

---

###  Upload de Imagem

```http
POST /image/upload
```

**Exemplo usando curl:**

```bash
curl -X POST http://localhost:5000/image/upload   -F "file=@sua_imagem.png"
```

---

###  Processar Imagem (executa o worker manualmente)

```http
POST /image/process
```

**Exemplo:**

```bash
curl -X POST http://localhost:5000/image/process
```

---

###  Listar imagens processadas

```http
GET /image/processed
```

**Resposta exemplo:**

```json
{
  "processed_files": [
    "imagem-processed-123.png"
  ]
}
```

---

###  Visualizar imagem processada

```http
GET /image/processed/<filename>
```

Acesse diretamente no navegador:

```
http://localhost:5000/image/processed/imagem-processada.png
```

---

## 🌐 Interface Web

Acesse no navegador:

```
http://localhost:5000/static/index.html
```

###  Funcionalidades da página:

- Upload de imagens
- Botão para processar
- Visualização direta das imagens processadas

---

##  Swagger - Documentação da API

A documentação Swagger é gerada automaticamente via **Flask-RESTX**.

Acesse em:

```
http://localhost:5000/
```



