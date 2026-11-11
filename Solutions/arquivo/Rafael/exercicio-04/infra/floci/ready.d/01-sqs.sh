#!/bin/sh
set -eu

echo "A criar infraestrutura"

aws sqs create-queue --queue-name livros-entrada.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false
aws sqs create-queue --queue-name livros-saida.fifo --attributes FifoQueue=true,ContentBasedDeduplication=false

aws s3 mb s3://romance
aws s3 mb s3://ficcao
aws s3 mb s3://outros

echo "Infraestrutura pronta"