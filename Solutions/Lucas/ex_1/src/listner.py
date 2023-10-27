from . import aws_utility

def listen_and_process():
    # While to keep checking if there is a new message
    print('Listening for items in the QUEUE...')

    # Creating pooling and saving dependencies
    try:
        sqs_client = aws_utility.aws_client('sqs')
        s3_client  = aws_utility.aws_client('s3')
    except:
        print('AWS connection failed...')
        return
    
    # Initianting listner
    while True:
        # Checks if there is a new message in the SQS
        message_object = aws_utility.pool_message(sqs_client)
        
        # If there is a new and valid message, tries to save it
        if message_object != False:
            print('---------------------------------------------')
            # Logging queue processing message
            print('Processing queue item with id: {}'.format(message_object['id']))

            # Putting the message into a bucket
            aws_utility.save_message(s3_client, message_object)

            print('---------------------------------------------')
