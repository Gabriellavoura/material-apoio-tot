# Importando bibliotecas
from flask import Flask
from utils.response import create_response

app = Flask(__name__)

stat_health = True

# Criando a rota de health tndo por base a função de criação de resposta.

@app.route('/health')
def health():

    # Chamando a função para criar uma resposta HTTP

    return create_response()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)