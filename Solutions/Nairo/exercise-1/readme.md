
# Material de Apoio ToT - Exercício 1
  

O objetivo do exercício é construir uma API flask com duas rotas não bloqueantes e paralelas, de forma que suporte processamentos longos (horas de duração):

### Rotas
- Rota `/` raiz da aplicação
- Rota `/health` para checar o healthcheck do container, mostrar filas e buckets existentes e o conteúdo de cada bucket.

### Variáveis de ambiente
- `ENDPOINT_URL`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `REGION_NAME`
- `INPUT_QUEUE_URL`
- `OUTPUT_QUEUE_URL`

### Dependências
- flask 3.0.0
- boto3 1.28.74
- pySqsListener 0.9.0
- requests 2.30.0
- gunicorn 21.2.0

### Executando o projeto
Para executar a API é necessário fazer o build da imagem com o comando `docker build -t app .
` e logo após executar a imagem com o comando `docker run -dp 5000:8000 app`