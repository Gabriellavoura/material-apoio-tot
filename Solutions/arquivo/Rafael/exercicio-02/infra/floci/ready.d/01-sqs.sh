#!/bin/sh
echo "Criando filas SQS FIFO"

awslocal sqs create-queue \
  --queue-name InputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false

awslocal sqs create-queue \
  --queue-name OutputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false

echo "Filas SQS criadas"