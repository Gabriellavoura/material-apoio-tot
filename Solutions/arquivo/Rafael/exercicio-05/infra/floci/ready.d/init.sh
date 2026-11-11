#!/bin/sh
set -eu

echo "Criando filas SQS"
aws sqs create-queue --queue-name livros-entrada.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false
aws sqs create-queue --queue-name livros-saida.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false

echo "Criando buckets S3"
aws s3 mb s3://romance
aws s3 mb s3://ficcao
aws s3 mb s3://outros

echo "Recursos criados"
