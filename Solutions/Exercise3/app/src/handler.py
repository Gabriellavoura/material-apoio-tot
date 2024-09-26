import logging
import tempfile
import json
from env import *
from tools.aws_utility import configure_sqs_or_s3_client, upload_file, write_message

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('log')

def upload_file_in_correct_bucket(s3_client, genre, file_path, object_name):
    
    if(genre == 'Scifi'):
        upload_file(s3_client, BUCKET_A, file_path=file_path, object_name=object_name)
        return
    else:
        upload_file(s3_client, BUCKET_B, file_path=file_path, object_name=object_name)
        return

def execute(event):
    
    logger.warning('execucao comecou')
    logger.warning(f'{event},{type(event)}')
    if(event is None):
        logger.warning('Evento veio none')
        return 
        
    genre = event['genre'] if event['genre'] is not None else 'Genero nao informado'
    title = event['title'] if event['title'] is not None else 'Titulo nao informado'
    file_id = event['id'] if event['id'] is not None else 'Id nao informado'
    
    s3_client = configure_sqs_or_s3_client('s3')
    sqs_client = configure_sqs_or_s3_client('sqs')
    temporary_file = tempfile.NamedTemporaryFile(mode="w+" , suffix='.json')
    json.dump(event, temporary_file)
    temporary_file.flush()

    upload_file_in_correct_bucket(s3_client, genre, file_path=temporary_file.name, object_name=event['title'])

    msg = { 'id':        file_id,
            'resource':  OUTPUT_QUEUE_NAME,
            'fileName':  title,
            'target':    genre
          }
    msg = json.dumps(msg)
    write_message(sqs_client, OUTPUT_QUEUE_URL, msg)
    
    logger.warning('execucao terminou')
    return 
