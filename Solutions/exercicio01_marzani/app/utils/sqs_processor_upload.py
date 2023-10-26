import os

from s3_upload        import *
from sqs_read_message import *
from dotenv           import load_dotenv

load_dotenv()


# Criando função de processar mensagem da fila SQS para testes.
def processar_message(response):
    try:

        # Desserialize a mensagem JSON em um dicionário Python
        message_data = response

        body = message_data['Messages'][0]['Body']

        body = json.loads(body)

        # Obtenha o nome do arquivo a ser salvo
        file_name = body['title'] + ".json"

        # Obtenha o nome do bucket com base no gênero (genre)
        genre = body['genre']
        bucket_name = genre  # Substitua com seu padrão de nome de bucket

        # Faça o upload do arquivo para o bucket no Amazon S3
        s3_client = instanciar_s3()

        with open(file_name, 'w') as file:
            json.dump(body, file)

        s3_client.upload_file(file_name, bucket_name, file_name)

        print(f'Arquivo {file_name} enviado para o bucket {bucket_name} com sucesso.')

        # Adicionando função para remover o arquivo localmente e deixar apenas no bucket.
        os.remove(file_name)
        return True
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        return False
    

response = read_message(sqs_client, os.getenv('SQS_IN'))
processar_message(response)

'''
Exemplo de mensagem
message = '{"id": "12345","title": "LoremIpsum","author": "John Doe","year": "1960","genre": "romance","summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,sed do eiusmod tempor incididuntut labore et dolore magna aliqua."}'
message2 = '{"id": "1234545","title": "Loremasasm","author": "John Doe","year": "1960","genre": "scifi","summary": "Lorem ipsum dolor sit amet, consectetur amagna aliqua."}'

processar_message(message)
processar_message(message2)

Realizar essa desserialização pegando a mensagem direto na inputqueue.fifo. 
'''