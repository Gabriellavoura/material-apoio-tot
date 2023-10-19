# Importando bibliotecas
from flask import Flask
from response import create_response

app = Flask(__name__)

stat_health = True

# Criando a rota de health tndo por base a função de criação de resposta.

@app.route('/health')
def health():

    # Criando um dicionário chamado de body com uma mensagem
    body = {
        "message": "Healthy"
    }

    # Chamando a função para criar uma resposta HTTP e o corpo acima.

    return create_response(200, body)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

