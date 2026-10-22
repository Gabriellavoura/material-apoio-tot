# :wave: Boas-vindas ao ToT

Olá! Que bom ter você aqui.

O **ToT (Text Of Things)** é o nosso projeto de pesquisa e desenvolvimento. Nele construímos o **vddb**, o sistema que o projeto entrega.

Este repositório é o seu **kit de boas-vindas**: reúne o que você precisa instalar, o que estudar e uma trilha de exercícios para praticar com as mesmas ferramentas que usamos no dia a dia.

> **Como estudar:** leia a documentação oficial de cada ferramenta (os links estão em cada guia), rode os exemplos e faça os exercícios. Vídeos ajudam a fixar, mas comece pela documentação.

---

## :rocket: Por onde começar

1. Leia o [checklist da primeira semana](docs/00-primeira-semana.md).
2. Prepare seu computador com o [guia de ambiente](docs/01-ambiente.md).
3. Siga os guias e os exercícios na ordem da trilha abaixo.

## :books: Guias

| # | Guia | O que você vai aprender |
|---|------|-------------------------|
| 00 | [Primeira semana](docs/00-primeira-semana.md) | Contas, acessos e a quem pedir ajuda |
| 01 | [Ambiente](docs/01-ambiente.md) | WSL, VSCode, Git, Python (uv), Docker e AWS CLI |
| 02 | [Git e GitHub](docs/02-git.md) | Branch, commit, Pull Request e versões |
| 03 | [AWS local com Floci](docs/03-aws-local-floci.md) | S3 e SQS rodando no seu computador |
| 04 | [Banco de dados](docs/04-banco-de-dados.md) | PostgreSQL e CloudBeaver (DBeaver) |
| 05 | [Imagens e OCR](docs/05-imagem-ocr.md) | OpenCV e Tesseract |
| 06 | [Inteligência Artificial](docs/06-ia.md) | IA local e assistentes de código |
| -- | [Glossário](docs/glossario.md) | Os termos técnicos explicados de forma simples |

## :zap: Trilha de exercícios

Cada exercício usa o que você aprendeu no anterior. Faça na ordem.

| # | Exercício | Guias de apoio |
|---|-----------|----------------|
| 01 | [Buckets S3 com Floci](Exercises/01-s3.md) | 01, 03 |
| 02 | [Filas SQS FIFO com Floci](Exercises/02-sqs-fifo.md) | 03 |
| 03 | [Sua primeira API com FastAPI](Exercises/03-api-fastapi.md) | 01 |
| 04 | [Worker: processando mensagens da fila](Exercises/04-worker.md) | 03 |
| 05 | [Salvando dados no PostgreSQL](Exercises/05-banco-de-dados.md) | 04 |
| 06 | [Desafio final: pipeline de imagens](Exercises/06-desafio-final.md) | todos |

Para não começar do zero, use o [projeto base](templates/projeto-base/). Ele já sobe com um comando: API, Floci, floci-ui, PostgreSQL e CloudBeaver.

## :hammer_and_wrench: Tecnologias

| Para quê | Ferramenta | Documentação oficial |
|----------|------------|----------------------|
| Editor | VSCode | [code.visualstudio.com/docs](https://code.visualstudio.com/docs) |
| Linux no Windows | WSL 2 | [learn.microsoft.com/windows/wsl](https://learn.microsoft.com/pt-br/windows/wsl/) |
| Versionamento | Git + GitHub | [git-scm.com/book/pt-br](https://git-scm.com/book/pt-br/v2) · [docs.github.com/pt](https://docs.github.com/pt) |
| Linguagem | Python 3.12+ | [docs.python.org/pt-br/3](https://docs.python.org/pt-br/3/) |
| Pacotes Python | uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Containers | Docker + Docker Compose | [docs.docker.com](https://docs.docker.com/) |
| API | FastAPI | [fastapi.tiangolo.com/pt](https://fastapi.tiangolo.com/pt/) |
| AWS (nuvem) | S3, SQS e boto3 | [docs.aws.amazon.com](https://docs.aws.amazon.com/) · [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) |
| Linha de comando AWS | AWS CLI v2 | [docs.aws.amazon.com/cli](https://docs.aws.amazon.com/cli/latest/userguide/) |
| AWS no seu computador | Floci + floci-ui | [floci.io/floci](https://floci.io/floci/) · [floci-ui](https://github.com/floci-io/floci-ui) |
| Banco de dados | PostgreSQL 18 | [postgresql.org/docs/18](https://www.postgresql.org/docs/18/) |
| Ver o banco | CloudBeaver / DBeaver | [dbeaver.com/docs/cloudbeaver](https://dbeaver.com/docs/cloudbeaver/) · [dbeaver.io](https://dbeaver.io/) |
| Banco no Python | SQLModel + psycopg | [sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com/) · [psycopg.org](https://www.psycopg.org/psycopg3/docs/) |
| Imagens | OpenCV | [docs.opencv.org/4.x](https://docs.opencv.org/4.x/) |
| OCR | Tesseract 5 | [tesseract-ocr.github.io](https://tesseract-ocr.github.io/) |
| Testes | pytest | [docs.pytest.org](https://docs.pytest.org/) |
| Qualidade de código | Ruff | [docs.astral.sh/ruff](https://docs.astral.sh/ruff/) |
| IA local | Ollama · llama.cpp | [docs.ollama.com](https://docs.ollama.com/) · [llama.cpp](https://github.com/ggml-org/llama.cpp) |

## :card_file_box: Soluções anteriores

A pasta [`Solutions/`](Solutions/) guarda soluções de ICs anteriores, como histórico. Elas usam a stack antiga (Flask e LocalStack) e servem só de consulta.

## :handshake: Contribuindo

Achou um link quebrado, um erro ou tem uma ideia de exercício? Abra uma *issue* ou um *Pull Request*. Veja como no [guia de Git](docs/02-git.md).

> Última revisão do material: outubro de 2026.
