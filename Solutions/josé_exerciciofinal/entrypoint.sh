#!/bin/bash

set -e

echo "Aguardando LocalStack iniciar..."

# Aguarda LocalStack responder na porta 4566
until curl -s http://localstack:4566/_localstack/health | grep '"s3": "running"' > /dev/null; do
  echo "Aguardando LocalStack estar pronto..."
  sleep 2
done

echo "LocalStack está pronto. Iniciando configuração..."

#echo "Limpando filas antigas (se existirem)..."
#awslocal sqs delete-queue --queue-url http://localhost:4566/000000000000/new-image-input.fifo || true
#awslocal sqs delete-queue --queue-url http://localhost:4566/000000000000/new-image-processed.fifo || true

#echo "Criando filas SQS..."
#awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
#awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "Criando buckets S3..."
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-processed

echo "Setup concluído com sucesso!"
