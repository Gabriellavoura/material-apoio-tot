# Desenvolvimento de uma API que suporta longas durações de processamento


### Ferramentas utilizadas:
- Git;

- Localstack;

- Flask;

- Docker;

- Gunicorn;

- PySQSListener.

### Descrição:
- API Flask, com duas rotas não bloqueantes:    

    - Rota `/health` para checar o healthcheck do container, que deve retornar o código http correto, conforme normas para uma API REST. Nesta API, a rota `/health` está retornando a healthcheck do localstack através de uma requisição GET. Ao realizar o GET nesta rota, o retorno terá a seguinte representação como base:

        ```json
        {
        "body": {
            "edition": "community",
            "services": {
            "acm": "available",
            ...
            },
            "version": "2.3.3.dev"
        },
        "statusCode": 200
        }
        ```

    - Rota `/` para realizar o pooling de mensagens na fila de entrada. Para isso, utilizou-se:

        - 2 Buckets do S3:
            - Um para salvar arquivos de Scifi;

            - Um para salvar arquivos de Romance.
            
        - 2 Filas SQS do tipo FIFO:
            - InputQueue - Para receber as mensagens que serão desserializadas para posterior upload nos respectivos buckets.

            - OutpuQueue - Irá ser utilizada para disparo de uma mensagem após o sucesso de realização do upload do JSON, possuindo dados de nome do arquivo e bucket.

Ao receber uma nova mensagem, a mesma será processada continuamente, ou seja, será desserealizada a mensagem recebida em um dicionário para consumir os valores. Para manter o processo monitorando a fila, utilizou-se o PySQSListener.

A mensagem irá conter:

```json
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

Sendo que:
- `title`: nome doo arquivo a ser salvo no bucket.
- `genre`: define qual bucket o arquivo será salvo. 

O arquivo consiste da própria mensagem, em formato json e será salvo, com extensão no bucket referente ao gênero do mesmo.

### Instalação:
..................
