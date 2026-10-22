# Glossário

Termos que aparecem no material, explicados de forma simples.

| Termo | O que significa |
|-------|-----------------|
| **API** | Um "balcão de atendimento" de um programa: outros programas fazem pedidos (requisições) e recebem respostas. |
| **AWS** | Amazon Web Services, a nuvem da Amazon. |
| **AWS CLI** | Programa de linha de comando para usar a AWS (ou o Floci) pelo terminal. |
| **boto3** | Biblioteca Python oficial para usar a AWS. |
| **Branch** | Uma linha paralela de trabalho no Git. Você muda o código nela sem afetar a `main`. |
| **Bucket** | A "pasta principal" do S3, onde os arquivos ficam guardados. |
| **CloudBeaver** | Versão web do DBeaver para ver e editar o banco de dados pelo navegador. |
| **Commit** | Um "ponto salvo" no histórico do Git, com uma mensagem explicando a mudança. |
| **Container** | Uma "caixa" isolada que roda um programa com tudo o que ele precisa. Criado a partir de uma **imagem**. |
| **Docker Compose** | Ferramenta para subir vários containers juntos a partir do arquivo `compose.yaml`. |
| **Endpoint / rota** | Um endereço da API, como `/health` ou `/upload`. |
| **`.env`** | Arquivo com configurações e senhas locais. **Nunca** vai para o Git. |
| **FastAPI** | Biblioteca Python para criar APIs. Gera a documentação (Swagger) sozinha. |
| **FIFO** | *First In, First Out*: o primeiro que entra é o primeiro que sai. |
| **Fila (SQS)** | Lugar onde um programa deixa mensagens para outro processar depois. |
| **Floci** | Programa que imita a AWS no seu computador, para estudar e testar sem custo. |
| **Healthcheck** | Rota ou comando que responde se o serviço está funcionando. |
| **Imagem (Docker)** | A "receita" pronta de um container, por exemplo `postgres:18`. |
| **LLM** | *Large Language Model*: modelo de IA que entende e gera texto, como os do ChatGPT e do Claude. |
| **OCR** | *Optical Character Recognition*: ler o texto que aparece em uma imagem. |
| **OpenAPI / Swagger** | Padrão para descrever uma API. O Swagger é a tela que mostra e testa as rotas (`/docs`). |
| **Polling** | Perguntar repetidamente "tem algo novo?". O worker faz polling na fila. |
| **PostgreSQL** | Banco de dados relacional (com tabelas, linhas e colunas). |
| **Pull Request (PR)** | Pedido para juntar as mudanças da sua branch na `main`, com revisão de outra pessoa. |
| **S3** | Serviço da AWS para guardar arquivos. |
| **SemVer** | Regra para numerar versões: `MAIOR.MENOR.CORREÇÃO`. |
| **SQL** | Linguagem para consultar e alterar dados no banco. |
| **SQLModel** | Biblioteca Python para usar o banco de dados escrevendo classes em vez de SQL. |
| **Tag** | Uma marca em um commit do Git, geralmente usada para versões (`v1.0.0`). |
| **Teste automatizado** | Código que confere se outro código funciona. Rodamos com `pytest`. |
| **uv** | Ferramenta que instala o Python e as bibliotecas do projeto. |
| **vddb** | O sistema que o projeto ToT constrói. |
| **Worker** | Programa que roda "nos bastidores", pegando tarefas de uma fila e processando. |
| **WSL** | *Windows Subsystem for Linux*: um Linux rodando dentro do Windows. |
