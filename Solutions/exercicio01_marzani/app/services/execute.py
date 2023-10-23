import logging
import json
from services.sqs_listener import instanciar_sqs
from services.s3_controller import instanciar_s3, upload_file

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

def execute(event):

    logger.warning("Aplicação Iniciada")

    logger.warning(f"Events -> {event}, TYPE: {type(event)}")

    try:
        sqs_client = instanciar_sqs()
        s3_client = instanciar_s3()

        #documents = read_message(sqs_client, URL_QUEUE_PDF)
        #logger.warning(f"received event-> {event}")
        # receiptHandle = event['Messages'][0]['ReceiptHandle']

        # req = event['Messages'][0]['Body']
        # print(event['Messages'][0]['Body'])
        # print(receiptHandle)
        message = json.loads(event['Message'])
        logger.warning(f"received message -> {message}")

        #data = json.dumps(events)

        logger.warning(f'Received data package: {message}, TYPE: {type(message)}')

        file_id = message["id"]

        file_name = message["title"] + ".json"
        logger.warning(f'file name: {file_name}')

        genre = message["genre"]

        logger.warning("Uploading JSON...")
        upload_json(s3_client, sqs_client, file_id, file_name, message)

        logger.warning('Aplicação feita.')
        return 1, genre

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
    
def upload_json(s3_client, sqs_client, file_id, file_name, event):

    if genre == "romance":
        upload_file(s3_client, "romance", event, file_id, file_name)
    

    #print(f'File Name: {file_name}')
    tg = event['target'].upper()
    QUEUE_NAME = ""
    if(tg == 'N381' or tg == 'LD'):
        QUEUE_NAME = NAME_QUEUE_N381
    elif (tg == 'ENAVAL'):
        QUEUE_NAME = NAME_QUEUE_ASSEMBLY
    elif (tg == 'JEA'):
        QUEUE_NAME = NAME_QUEUE_SUPPLIERS
    else:
        logger.warning(f"Invalid target: {tg}")

    msg = {'id':        file_id,
           'resource':  BUCKET_FORMUND,
           'fileName':  file_name,
           'target':    tg,
           'projectName': event["projectName"],
           'size':      size,
           'updatedAt': current_time}

    logger.warning('--- FORMUND: Publishing ---')
    logger.warning('--------- LOG DAS FILAS ---------------')
    logger.warning(f"(ENTRADA) FILA OCR: {NAME_QUEUE_HOCR}")
    logger.warning(f"(SAIDA) FILA ASSEMBLY: {NAME_QUEUE_ASSEMBLY}")
    logger.warning(f"(SAIDA) FILA N381: {NAME_QUEUE_N381}")
    logger.warning(f"(SAIDA) FILA SUPPLIERS: {NAME_QUEUE_SUPPLIERS}")
    logger.warning('------------------------------')

    logger.warning('Queue:')
    logger.warning(QUEUE_NAME)
    logger.warning('Message:')
    logger.warning(msg)
    final_msg = json.dumps(msg)

    formund_queue_url = get_queue_url(sqs_client, QUEUE_NAME)
    if write_message(sqs_client, formund_queue_url, final_msg):

        logger.warning("Msg delivered.")
    else:
        logger.warning("Can't send the message")