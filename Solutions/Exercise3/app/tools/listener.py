from sqs_listener import SqsListener
from src.handler import execute

class ProcessSQSListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        execute(body)
        