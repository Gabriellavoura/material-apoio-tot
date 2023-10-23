from s3_upload import *

def processar_message(message):
    try:
        # Desserialize a mensagem JSON em um dicionário Python
        message_data = json.loads(message)

        # Obtenha o nome do arquivo a ser salvo
        file_name = message_data['title'] + ".json"

        # Obtenha o nome do bucket com base no gênero (genre)
        genre = message_data['genre']
        bucket_name = genre  # Substitua com seu padrão de nome de bucket

        # Faça o upload do arquivo para o bucket no Amazon S3
        s3_client = instanciar_s3()

        with open(file_name, 'w') as file:
            json.dump(message_data, file)

        s3_client.upload_file(file_name, bucket_name, file_name)

        print(f'Arquivo {file_name} enviado para o bucket {bucket_name} com sucesso.')
        return True
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        return False
    
'''
Exemplo de mensagem
message = '{"id": "12345","title": "LoremIpsum","author": "John Doe","year": "1960","genre": "romance","summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit,sed do eiusmod tempor incididuntut labore et dolore magna aliqua."}'
message2 = '{"id": "1234545","title": "Loremasasm","author": "John Doe","year": "1960","genre": "scifi","summary": "Lorem ipsum dolor sit amet, consectetur amagna aliqua."}'

CONSEGUI FAER FUNCIONAR /\ É NESSE FORMATO QUE TEM QUE ESTAR A MESSAGE

processar_message(message)
processar_message(message2)

Realizar essa desserialização pegando a mensagem direto na inputqueue.fifo. 
'''