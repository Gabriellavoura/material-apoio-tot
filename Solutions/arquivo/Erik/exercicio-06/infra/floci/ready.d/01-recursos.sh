#!/bin/sh
set -eu

# Buckets do pipeline de imagens
aws s3 mb s3://image-input
aws s3 mb s3://image-output

# Filas FIFO: entrada (API -> worker) e saída (worker -> aviso de conclusão)
aws sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true
aws sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true