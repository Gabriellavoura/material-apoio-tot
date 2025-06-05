#!/bin/bash

# Criar uma requisição de teste para o endpoint de upload
echo "Testando o endpoint de upload de imagem..."

# Verificar se a imagem de teste existe
if [ ! -f "test_image.png" ]; then
    echo "Erro: Imagem de teste não encontrada. Execute primeiro o script create_test_image.py"
    exit 1
fi

# Enviar a imagem para o endpoint de upload
curl -X POST -F "image=@test_image.png" http://localhost:5000/upload

echo -e "\n\nTeste concluído!"
