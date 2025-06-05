#!/bin/bash
echo "⏳ Inicializando recursos AWS no LocalStack..."

# Criar buckets S3
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-processed

# Criar filas FIFO SQS
awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "✅ Buckets e filas criados com sucesso!"
