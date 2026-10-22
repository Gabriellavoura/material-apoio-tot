#!/bin/sh
# Roda automaticamente quando o Floci termina de subir.
# Docs: https://floci.io/floci/configuration/initialization-hooks/
# Crie aqui os buckets e filas que a sua aplicação precisa.
set -eu

echo "Criando buckets..."
aws s3 mb s3://exemplo-bucket

echo "Criando filas FIFO..."
aws sqs create-queue --queue-name exemplo-fila.fifo --attributes FifoQueue=true

echo "Recursos criados!"
