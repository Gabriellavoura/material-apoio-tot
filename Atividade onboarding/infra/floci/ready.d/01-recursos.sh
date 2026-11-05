#!/bin/sh
# Roda automaticamente quando o Floci termina de subir.
# Docs: https://floci.io/floci/configuration/initialization-hooks/
# Crie aqui os buckets e filas que a sua aplicação precisa.
set -eu

echo "Criando buckets..."
for bucket in romance ficcao outros image-input image-output; do
  aws s3 mb "s3://$bucket" 2>/dev/null || true
done

echo "olá, ToT" > /tmp/onboarding-guilherme.txt
aws s3 cp /tmp/onboarding-guilherme.txt s3://outros/onboarding-guilherme.txt

echo "Criando filas FIFO..."
for queue in livros-entrada.fifo livros-saida.fifo new-image-input.fifo new-image-processed.fifo; do
  aws sqs create-queue --queue-name "$queue" \
    --attributes FifoQueue=true,ContentBasedDeduplication=false 2>/dev/null || true
done

echo "Recursos criados!"
