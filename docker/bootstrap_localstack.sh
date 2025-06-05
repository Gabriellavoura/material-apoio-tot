#!/bin/bash

set -e

echo "🔧 Inicializando recursos no LocalStack..."

# Criação das filas FIFO
awslocal sqs create-queue \
  --queue-name new-image-input.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=true

awslocal sqs create-queue \
  --queue-name new-image-processed.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=true

# Criação dos buckets S3
awslocal s3 mb s3://image-input || true
awslocal s3 mb s3://image-processed || true

# Upload opcional de imagem de teste (caso exista /docker/teste.png)
if [ -f "/docker/teste.png" ]; then
  cp /docker/teste.png /tmp/teste.png
  awslocal s3 cp /tmp/teste.png s3://image-input/teste.png

  awslocal sqs send-message \
    --queue-url http://localhost:4566/000000000000/new-image-input.fifo \
    --message-body teste.png \
    --message-group-id image-processing
fi

echo "✅ Recursos criados com sucesso no LocalStack."
