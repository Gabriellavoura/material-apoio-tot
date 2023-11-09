import logging
import json
import os


from dotenv                     import load_dotenv
from utils.sqs_instance         import *
from utils.s3_instance          import *
from utils.s3_upload            import *
from utils.sqs_read_message     import *
from utils.sqs_write_message    import write_message

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


# Função para a execução a partir do listener.
def execute(event):

    logger.warning("Monitoramento...")

    logger.warning(f"Events -> {event}, TYPE: {type(event)}")

    try:
        s3_client = instanciar_s3()

        # Pegando o corpo da mensagem da InputQueue e fazendo o processamento.

        body = event
        logger.warning(f"received message -> {body}")

        logger.warning(f'Received data package: {body}, TYPE: {type(body)}')

        file_name = body["title"] + ".json"
        logger.warning(f'file name: {file_name}')

        # Pegando o tipo do gênero para a seleção do bucket. Se o nome estiver de acordo com os buckets existentes
        # o upload será feito no bucket.
        genre = body["genre"]
        bucket_name = genre

        with open(file_name, 'w') as file:
            json.dump(body, file)

        logger.warning("Finalizando processamento.")

        logger.warning("Uploading JSON...")

        # Fazendo o upload no bucket.
        s3_client.upload_file(file_name, bucket_name, file_name)

        logger.warning(f'Arquivo {file_name} enviado para o bucket {bucket_name} com sucesso.')

        mensagem = f'Arquivo {file_name} enviado para o bucket {bucket_name} com sucesso.'
        # Adicionando função para escrever mensagem na outputqueue.fifo retornando a mensagem de sucesso ao 
            # Fazer upload do json no respectivo bucket.

        write_message(sqs_client, os.getenv('SQS_OUT'), mensagem)
        logger.warning(f'Mensagem de sucesso com {file_name} e {bucket_name} disparada para a OutputQueue')

        # Adicionando função para remover o arquivo localmente e deixar apenas no bucket.
        os.remove(file_name)
        return 1

    except TypeError as t:
        print("TypeError -> " + str(t))
        logger.error('TypeError -> ', exc_info=True)
        return -1
    except KeyError as k:
        print("KeyError -> "+str(k))
        logger.error('KeyError -> ', exc_info=True)
        return -1
    except MemoryError as m:
        print("MemoryError -> "+str(m))
        logger.error('MemoryError -> ', exc_info=True)
        return -1
    except IndexError as i:
        print("IndexError -> "+str(i))
        logger.error('IndexError -> ', exc_info=True)
        return -1
    except AttributeError as a:
        print("AttributeError -> "+str(a))
        logger.error('AttributeError -> ', exc_info=True)
        return -1
    except ImportError as i:
        print("ImportError -> "+str(i))
        logger.error('ImportError -> ', exc_info=True)
        return -1
    except Exception as e:
        print("Exeption -> "+str(e))
        logger.error('Exeption -> ', exc_info=True)
        return -1