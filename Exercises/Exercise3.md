# Exercise 3: Developing an API that supports long-running processing

**Objetivo**: Criar uma API flask, com duas rotas não bloqueantes, que leia o conteúdo de uma mensagem sqs e publique arquivos em buckets s3.


**Descrição**

Criar uma API flask, com duas rotas não bloqueantes e paralelas, de forma que suporte processamentos longos (horas de duração):

*  Rota `/health` para checar o healthcheck do container, que deve retornar o código http correto, conforme normas para uma api REST.

* Rota `/` para fazer pooling de mensagens na fila de entrada.

Ao receber uma nova mensagem a mesma deve ser processada, ou seja deve-se desserealizar a mensagem recebida em um dicionario, para consumir os valores.

A mensagem irá conter:

```Json
    {
     "id": "12345",
     "title": "LoremIpsum",
     "author": "John Doe",
     "year": "1960",
     "genre": "romance",
     "summary": "Lorem ipsum dolor sit amet, 
                 consectetur adipiscing elit,
                 sed do eiusmod tempor incididunt
                 ut labore et dolore magna aliqua."
    }
```

Onde os valores das chaves:

 * `title`: Nome do arquivo a ser salvo no bucket.
 * `genre`: Define qual bucket o arquivo deve ser salvo.

O arquivo consiste da própria mensagem, em formato json, resultando em:

```Json
    LoremIpsum.json

        {"id": "12345",
        "title": "LoremIpsum",
        "author": "John Doe",
        "year": "1960",
        "genre": "romance",
        "summary": "Lorem ipsum dolor sit amet, 
                    consectetur adipiscing elit,
                    sed do eiusmod tempor incididunt
                    ut labore et dolore magna aliqua."}

```
Após o arquivo deve ser salvo, com extensão no bucket referente ao gênero do mesmo.

## Arquitetura

A arquitetura pode ser descrita conforme figura a seguir:
![Architecture](../img/Exercise%201%20-%20Architecture.png)


## Requirements

Segue algumas bibliotecas necessárias para resolução do exercício:

* [gunicorn](https://gunicorn.org/)
* [gevent](https://pypi.org/project/gevent/)
* [boto3](https://pypi.org/project/boto3/)
* [pySQSListener](https://pypi.org/project/pySqsListener/)


## Folder structure

Segue uma sugestão de organização dos arquivos

```console
app
├── __init__.py
├── tools
│   ├── __init__.py
│     ├── listener.py
│     └── aws_utility.py
├── src
│   ├── __init__.py
│   └── handler.py
├── dockerfile
├── env.py
├── gunicorn_starter.sh
├── main.py
└── requirements.txt
```

## Outro

Arquivo para criação do ambiente via localstack.

Este arquivo será utilizado para teste da aplicação.

```shell
#!/bin/sh

# Sets the localstack settings
export AWS_ACCOUNT_ID="localstack"
export AWS_PROFILE="localstack"


# Create the queues using awslocal
echo "Creating the queues ..."
awslocal sqs create-queue --queue-name InputQueue.fifo --attributes FifoQueue=true
awslocal sqs create-queue --queue-name OutputQueue.fifo --attributes FifoQueue=true


# Create the buckets
echo "Creating buckets ..."
awslocal s3api create-bucket --bucket scifi
awslocal s3api create-bucket --bucket romance


# Sends a message to the pdf-new queue
echo "Sending a message to the InputQueue..."
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "test" --message-deduplication-id "test" --message-body '{"id": "12345", "title":"LoremIpsum", "author": "John Doe", "year":"1960", "genre":"Scifi", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}'

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "test1" --message-deduplication-id "test1" --message-body '{"id": "12345", "title":"LoremIpsum", "author": "John Doe", "year":"1960", "genre":"romance", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}'
```


**Lembrando que o código deve ser publicado no github e deve ser feito utilizando containers docker.**



