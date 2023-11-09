# Importando bibliotecas
import os

from flask                      import Flask, jsonify
from threading                  import Thread
from utils.response             import create_response
from dotenv                     import load_dotenv
from utils.listener             import ProcessSQSListener

load_dotenv()

app = Flask(__name__)

# Defina rotas e funções para o blueprint
@app.route('/health', methods=['GET'])
def health_check():
    # Chamando a função para criar uma resposta HTTP
    return create_response()

@app.route('/', methods=['GET'])
def receive_message():
    # return jsonify({'Application': 'Running Polling'}), 200
    return jsonify({'Application': 'Running Polling'}), 200


# Função de execução do listener.
def process():

    queue_url = os.getenv('SQS_IN')

    process_listener = ProcessSQSListener('InputQueue',
                                          endpoint_name=os.getenv('ENDPOINT_URL'),
                                          aws_access_key=os.getenv('KEY_ID'),
                                          aws_secret_key=os.getenv('ACCESS_KEY'),
                                          queue_url=queue_url,
                                          region_name=os.getenv('REGION'),
                                          force_delete=True)
    
    print("LISTEN EM EXECUÇÃO")
    process_listener.listen()

listen = Thread(target=process)
listen.start()