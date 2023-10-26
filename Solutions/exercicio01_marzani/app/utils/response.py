import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL')

def create_response():

    # Fazendo a requisição GET pra healthcheck do localstack e usando de base os dados pra health
    # da própria api

    resposta = requests.get(URL)
    print(resposta)

    data = json.loads(resposta.text)
    print(data)

    status_code = resposta.status_code
    print(status_code)

    # Função para criar a resposta da API.
        # - STATUS_CODE: código do status
        # - RESPONSE_DATA: dados da resposta
    
    try:
        return {
            "statusCode": status_code,
            "body": data
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }