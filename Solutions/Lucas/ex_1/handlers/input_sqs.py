import json
from   flask import request, Response
from   src import data_validation, aws_utility


def handle():
    print('---------------------------------------------')
    print('PUTTING MESSAGE INTO QUEUE')

    raw_data   = request.data
    object     = data_validation.validate_pooling_data(raw_data)
    input_data = json.dumps(object)

    if not object:
        status = 400
        body = json.dumps({
            'message': 'Invalid message',
            'status': status,
        })
    
    elif (aws_utility.input_sqs(input_data)):
        print('Message putted into QUEUE')
        status = 200
        body = json.dumps({
            'message': 'Message putted into QUEUE',
            'status': status,
        })
    else:
        status = 500
        body = json.dumps({
            'message': 'Something went wrong...',
            'status': status,
        })
    print('---------------------------------------------')
    
    return Response(response=body, status=status)
