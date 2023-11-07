from sqs_listener import SqsListener
from app.src.handler import execute

class ProcessSQSListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        try:
            execute(body)
        except Exception as err:
            return err