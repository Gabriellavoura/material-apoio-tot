# Exercício 02 · Filas SQS FIFO com Floci

**Objetivo:** criar duas filas FIFO, enviar mensagens, ler e apagar mensagens usando a AWS CLI.

**Antes de começar:** leia a parte de [filas FIFO no guia 03](../docs/03-aws-local-floci.md#filas-fifo).

## Passo a passo

1. Suba o Floci (o mesmo `compose.yaml` do [Exercício 01](01-s3.md)) e confira se ele está no ar:

   ```shell
   docker compose up -d
   curl http://localhost:4566/_floci/health
   ```

2. Crie a fila de entrada `InputQueue.fifo`:

   ```shell
   aws --profile floci sqs create-queue --queue-name InputQueue.fifo \
     --attributes FifoQueue=true,ContentBasedDeduplication=false
   ```

   > Atenção: **não** coloque espaço depois da vírgula em `--attributes`.

3. Crie a fila de saída `OutputQueue.fifo` do mesmo jeito.

4. Liste as filas e guarde a URL da `InputQueue.fifo`:

   ```shell
   aws --profile floci sqs list-queues
   ```

5. Envie uma mensagem para a `InputQueue.fifo` (troque `<url-da-fila>` pela URL do passo 4):

   ```shell
   aws --profile floci sqs send-message \
     --queue-url <url-da-fila> \
     --message-body '{"titulo": "Dom Casmurro", "genero": "romance"}' \
     --message-group-id livros \
     --message-deduplication-id livro-001
   ```

6. Leia a mensagem:

   ```shell
   aws --profile floci sqs receive-message --queue-url <url-da-fila>
   ```

   > Copie o valor de `ReceiptHandle` da resposta. Você vai precisar dele para apagar a mensagem.

7. Apague a mensagem (é assim que o programa avisa a fila que terminou o trabalho):

   ```shell
   aws --profile floci sqs delete-message --queue-url <url-da-fila> \
     --receipt-handle <receipt-handle>
   ```

8. Veja as filas no floci-ui, em `http://localhost:4500`.

## Para pensar

- Envie **duas** mensagens com o **mesmo** `--message-deduplication-id`. Quantas chegam na fila? Por quê?
- O que acontece se você ler uma mensagem e **não** apagá-la? Espere 30 segundos e leia de novo. Pesquise o que é *visibility timeout* na [documentação do SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html).

## Entrega

No mesmo repositório do Exercício 01: um script que cria as duas filas no `ready.d` e um README com as respostas do "Para pensar".
