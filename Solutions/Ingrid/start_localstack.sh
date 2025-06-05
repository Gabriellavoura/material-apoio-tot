#!/bin/bash

# Iniciar o LocalStack
echo "Iniciando o LocalStack..."
docker-compose up -d

# Aguardar o LocalStack iniciar
echo "Aguardando o LocalStack iniciar..."
sleep 10

# Configurar recursos AWS
echo "Configurando recursos AWS..."
source venv/bin/activate
python setup_aws_resources.py

echo "Configuração concluída!"
