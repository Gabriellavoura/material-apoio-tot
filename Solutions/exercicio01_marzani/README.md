# Desenvolvimento de uma API que suporta longas durações de processamento

### Objetivo:
- Criação de uma API Flask, com duas rotas não bloqueantes.
- Essa API Flask precisa ler o conteúdo de uma mensagem SQS e publicar arquivos em buckets s3.

### Descrição:

- Rota `/health` para checar o healthcheck do container, que deve retornar o código http correto, conforme normas para uma API REST.
- Rota `/` para realizar o pooling de mensagens na fila de entrada.

Ao receber uma nova mensagem, a mesma deve ser processada, ou seja, deve-se desserealizar a mensagem recebida em um dicionário para consumir os valores.

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
- `title`: nome o arquivo a ser salvo no bucket.
- `genre`: define qual bucket o arquivo será salvo. 

O arquivo consiste da própria mensagem, em formato json e deve ser salvo, com extensão no bucket referente ao gênero do mesmo.

- Utilizará-se 2 buckets:
    - Um para salvar arquivos de Scifi;
    - Um para salvar arquivos de Romance.

- Utilizará-se 2 filas SQS do tipo FIFO:
    - InputQueue
    - OutputQueue

### Ferramentas utilizadas:
- Git
- Localstack
- Flask
- Docker