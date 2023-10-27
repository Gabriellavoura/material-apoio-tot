from   flask     import Response
from   src       import listner
import threading
import gevent
import json

def handle():
    #gevent.spawn(listner.listen_and_process)
    thread = threading.Thread(target=listner.listen_and_process)
    thread.start()

    body = json.dumps({
            'message': 'Pooling has started',
            'status': 200
    })
    return Response(response=body, status=200)
