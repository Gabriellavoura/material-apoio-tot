#!/bin/sh
set -eu

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

api="http://localhost:8000"
livro_id="teste-e2e-$(date +%s)"

curl --fail --silent --show-error \
  -X POST "$api/livros" \
  -H "Content-Type: application/json" \
  -d "{\"id\":\"$livro_id\",\"titulo\":\"Livro de teste\",\"autor\":\"Autor de teste\",\"ano\":2026,\"genero\":\"romance\",\"resumo\":\"Fluxo ponta a ponta pelo onboarding.\"}" \
  >/dev/null

tentativas=0
while [ "$tentativas" -lt 120 ]; do
  resposta=$(curl --fail --silent "$api/livros/$livro_id")
  status=$(printf '%s' "$resposta" | python3 -c 'import json, sys; print(json.load(sys.stdin)["status"])')

  if [ "$status" = "processado" ]; then
    break
  fi

  tentativas=$((tentativas + 1))
  sleep 1
done

if [ "${status:-}" != "processado" ]; then
  echo "Livro não foi processado no prazo esperado." >&2
  exit 1
fi

fila_saida=$(aws --endpoint-url=http://localhost:4566 sqs get-queue-url \
  --queue-name livros-saida.fifo --query QueueUrl --output text)

mensagem=$(aws --endpoint-url=http://localhost:4566 sqs receive-message \
  --queue-url "$fila_saida" \
  --max-number-of-messages 10 \
  --output json)

receipt=$(printf '%s' "$mensagem" | LIVRO_ID="$livro_id" python3 -c '
import json
import os
import sys

dados = json.load(sys.stdin)
for mensagem in dados.get("Messages", []):
    if os.environ["LIVRO_ID"] in mensagem["Body"]:
        print(mensagem["ReceiptHandle"])
        break
')

if [ -z "$receipt" ]; then
  echo "Nenhuma mensagem encontrada na fila de saída." >&2
  exit 1
fi

aws --endpoint-url=http://localhost:4566 sqs delete-message \
  --queue-url "$fila_saida" \
  --receipt-handle "$receipt"

printf '%s\n' "$resposta"
