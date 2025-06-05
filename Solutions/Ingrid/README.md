# Pipeline-de-Processamento-de-Imagens-com-Flask-e-AWS

Este projeto implementa um pipeline de processamento de imagens utilizando Flask e serviços AWS simulados via LocalStack. O sistema permite que clientes enviem imagens PNG via API, que são armazenadas no S3, processadas com OpenCV e notificadas via filas SQS.

## Estrutura do Projeto

```
Pipeline-de-Processamento-de-Imagens-com-Flask-e-AWS/
├── templates/                   # Templates HTML, se houver
│   └── index.html               # Exemplo de página (se usado Flask frontend)
├── .gitignore                   # Ignorar venv, __pycache__, etc.
├── README.md                    # Documentação
├── docker-compose.yml           # Arquitetura com LocalStack e Flask
├── app/                          # Código principal da aplicação
├── image.png                    # Exemplo de imagem para testes
├── image_processor.py       # Processamento de imagem com OpenCV
├── main.py                      # Arquivo principal que chama o app Flask
├── requirements.txt             # Dependências do projeto
├── routes.py                # Rotas da API
├── s3_service.py            # Interação com S3 (LocalStack ou AWS)
├── setup_aws_resources.py   # Criação de buckets e filas
├── sqs_service.py           # Interação com filas SQS
├── __init__.py              # Inicialização da app Flask
├── start_app.sh             # Script para iniciar o app
├── start_localstack.sh      # Script para iniciar o LocalStack
├── test_upload.sh           # Script de teste de envio│   
├── worker.py                # Consumidor das mensagens SQS   

```

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- LocalStack

## Dependências

- Flask: Framework web
- Boto3: SDK AWS para Python
- OpenCV: Biblioteca de processamento de imagens
- Pillow: Biblioteca de manipulação de imagens
- LocalStack: Emulador de serviços AWS

## Configuração e Execução

### 1. Configuração do Ambiente

Clone o repositório e configure o ambiente virtual:

```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Iniciar o LocalStack e Configurar Recursos AWS

No primeiro terminal (fora do venv)
```bash
# Iniciar o LocalStack e criar recursos AWS
/pipeline-flask# docker-compose up -d
```
No segundo terminal (dentro do venv)
````bash
# - Executa o script Python que cria os recursos AWS no LocalStack, ou seja:
# - Cria os buckets S3 (como image-input e image-processed)
# - Cria as filas SQS FIFO (new-image-input.fifo, new-image-processed.fifo)
pipeline-flask# python setup_aws_resources.py
````
````bash
# Inicia o worker, que fica escutando a fila SQS (new-image-input.fifo) para processar imagens enviadas ao bucket. Ou seja, esse processo fica rodando em background processando as imagens.
python worker.py
````
No terceiro terminal (dentro do venv)
````bash
# - Caso necessário: Define variáveis de ambiente para o acesso AWS, que são necessárias para o SDK (boto3) funcionar, mesmo que você esteja usando LocalStack com credenciais falsas.
# - Essas variáveis simulam as credenciais para autenticação local.
AWS_ACCESS_KEY_ID=testst
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
````
````bash
# Inicia a aplicação Flask que expõe a interface web para upload e visualização das imagens processadas.
python main.py
````

A aplicação estará disponível em `http://127.0.0.1:5000 ou http://localhost:5000`.

### Como usar a interface

Abra seu navegador e acesse: http://localhost:5000 (ou o IP/porta que o Flask estiver usando).

Na página principal:

- Use o formulário para enviar uma nova imagem .png.
- Se a imagem já foi processada, verá a imagem original e a imagem processada exibidas.
- Caso o processamento ainda esteja em andamento, uma mensagem indicará isso.
- Uma lista das imagens existentes no bucket também estará disponível para navegação.

## Fluxo de Funcionamento

1. **Upload de Imagem**:
   - Cliente envia imagem PNG para o endpoint `/upload`
   - Imagem é armazenada no bucket S3 `image-input`
   - Mensagem é enviada para a fila SQS `new-image-input.fifo`

2. **Processamento de Imagem**:
   - Worker realiza polling na fila `new-image-input.fifo`
   - Ao receber mensagem, recupera a imagem do bucket S3 `image-input`
   - Processa a imagem com OpenCV (binarização)
   - Salva a imagem processada no bucket S3 `image-processed`
   - Envia mensagem para a fila SQS `new-image-processed.fifo`


## Detalhes da Implementação

### API Flask

A API Flask expõe um endpoint `/upload` que aceita requisições POST com imagens PNG. O endpoint valida a imagem, gera um ID único, faz upload para o S3 e envia uma mensagem para a fila SQS.

### Worker

O worker é executado em uma thread separada dentro da mesma aplicação Flask. Ele realiza polling contínuo na fila SQS, processa as imagens recebidas e envia notificações de conclusão.

### Processamento de Imagem

O processamento de imagem utiliza OpenCV para aplicar uma binarização simples na imagem original, convertendo-a para preto e branco.

### Uso de HTML para Upload e Visualização

O projeto inclui um arquivo HTML (upload.html) que apresenta:
- Um formulário para envio de imagens .png para o bucket S3 de entrada.
- Uma lista interativa das imagens armazenadas no bucket.
- Visualização lado a lado da imagem original e da imagem processada (após processamento).
- Mensagens de status para indicar o progresso.

## Observações

- Todas as filas SQS são do tipo FIFO (First-In-First-Out)
- O sistema utiliza IDs únicos (UUID) para rastrear imagens durante todo o pipeline
- O LocalStack simula os serviços AWS localmente, sem necessidade de credenciais reais
- O worker e a API são executados no mesmo processo para simplificar a implantação
