import logging

from sqs_listener import SqsListener
from utils.processor_execute      import execute

class ProcessSQSListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        try:
            execute(body)
        except Exception as e:
            print(f"Processor Exception -> {e}")
            logging.error(f"Processor Exception -> {e}")