import json

def create_response(status_code, response_data):

    # Função para criar a resposta da API. Os parâmetros são:
        # - STATUS_CODE: código do status
        # - RESPONSE_DATA: dados da resposta
    
    try:
        return {
            "statusCode": status_code,
            "body": json.dumps(response_data, indent=4)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }