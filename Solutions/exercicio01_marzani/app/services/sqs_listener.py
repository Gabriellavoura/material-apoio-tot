import logging

from sqs_listener import SqsListener

class ProcessSQSListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        try:
            execute(body)
        except Exception as e:
            print(f"Processor Exception -> {e}")
            logging.error(f"Processor Exception -> {e}")