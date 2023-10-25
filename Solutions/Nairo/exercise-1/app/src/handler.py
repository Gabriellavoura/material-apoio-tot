import json
import logging
from app.tools.aws_utility import *
from app.env import *

def execute(event):
    try:
        logging.info(f"processando event: {event} ---> tipo: {type(event)}")
        s3_client = instantiate_aws_client('s3')
        sqs_client = instantiate_aws_client('sqs')

        file_key = event['title'] + '.json'
        bucket_name = event['genre']
        message_body = json.dumps(event, indent=2)

        upload_file(s3_client, bucket_name, file_key, message_body)
        logging.info(f"upload no bucket {bucket_name} concluído")

        receipt_handle = event['ReceiptHandle']
        delete_message(sqs_client, INPUT_QUEUE_URL, receipt_handle)

        write_message(sqs_client, OUTPUT_QUEUE_URL, message_body)
        logging.info("body da mensagem enviado para a fila de output")
    
    except Exception as e:
        logging.error(e)