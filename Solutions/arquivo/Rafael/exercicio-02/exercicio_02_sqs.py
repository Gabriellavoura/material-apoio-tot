import boto3
import json
import time

sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

def enviar_mensagem_livro(livro_dict):
    queue_url = sqs.get_queue_url(QueueName="InputQueue.fifo")["QueueUrl"]
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(livro_dict),
        MessageGroupId="livros-grupo",
        MessageDeduplicationId=str(livro_dict["id"]),
    )
    print(f"+ Mensagem enviada com sucesso ID: {response.get('MessageId')}")
    return queue_url

def receber_e_deletar_mensagem(queue_url):
    print("* A ler a fila SQS")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=2
    )
    
    mensagens = response.get("Messages", [])
    if not mensagens:
        print("- Nenhuma mensagem encontrada na fila")
        return

    for msg in mensagens:
        print(f"+ Mensagem recebida (Body): {msg['Body']}")
        receipt_handle = msg["ReceiptHandle"]
        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("+ Mensagem apagada da fila com sucesso")

if __name__ == "__main__":
    print("Iniciando Teste SQS FIFO")
    livro_teste = {"id": 1, "titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien"}
    
    url_da_fila = enviar_mensagem_livro(livro_teste)
    
    time.sleep(1)
    
    receber_e_deletar_mensagem(url_da_fila)
    print("=== Teste Concluído ===")