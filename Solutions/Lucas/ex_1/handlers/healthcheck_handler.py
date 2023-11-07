from   flask import Response
import json

def handle():
    body = json.dumps({
        'message': 'API is up',
        'status': 200,
    })

    return Response(response=body, status=200)
