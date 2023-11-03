from . import aws_utility
import logging

def listen_and_process():
    """ Funtion to listen and process 
        new messages in the QUEUE. 
        """

    # While to keep checking if there is a new message
    logging.warning('Listening for items in the QUEUE...')

    # Creating pooling and saving dependencies
    try:
        sqs_client = aws_utility.aws_client('sqs')
        s3_client  = aws_utility.aws_client('s3')
    except:
        logging.warning('AWS connection failed...')
        return
    
    # Initianting listner
    while True:
        # Checks if there is a new message in the SQS
        message_object = aws_utility.pool_message(sqs_client)
        
        # If there is a new and valid message, tries to save it
        if message_object != False:
            logging.warning('---------------------------------------------')
            # Logging queue processing message
            logging.warning('Processing queue item with id: {}'.format(message_object['id']))

            # Putting the message into a bucket
            aws_utility.save_message(s3_client, message_object)

            logging.warning('---------------------------------------------')
