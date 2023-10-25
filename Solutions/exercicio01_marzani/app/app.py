# Importando bibliotecas
import os

from flask                      import Flask
from utils.response             import create_response
from utils.sqs_instance         import instanciar_sqs
from dotenv                     import load_dotenv
from utils.listener             import ProcessSQSListener

load_dotenv()

app = Flask(__name__)

stat_health = True

# Criando a rota de health tndo por base a função de criação de resposta.

'''@app.route('/health')
def health():

    # Chamando a função para criar uma resposta HTTP

    return create_response()'''


@app.route('/')
def process():

    # Instanciando cliente SQS
    sqs_client = instanciar_sqs()

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
process()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)