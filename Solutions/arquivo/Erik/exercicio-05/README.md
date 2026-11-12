# Trilha_exercicio_TOT

Repositório utilizado para trilha de exercícios do ToT.

## Exercício 03: API de livros com FastAPI

API que recebe os dados de um livro, valida e envia como mensagem para uma fila SQS FIFO (`livros-entrada.fifo`), rodando localmente com o Floci.

### Rotas

| Rota | Função dela |
|------|-----------|
| `GET /health` | Responde `200` com `{"status": "ok"}` quando a API está no ar |
| `POST /livros` | Valida o livro, salva no banco com `status = recebido`, envia para a fila e responde `202 Accepted` |
| `GET /livros/{id}` | Devolve os dados e o status do livro, ou `404` se ele não existir |
| `GET /livros` | Lista os livros. Aceita o filtro opcional `?status=processado` |

Se faltar um campo ou se o `ano` não for um número, a API responde `422`. Se o `id` já estiver cadastrado, responde `409 Conflict`.

O `status` do livro começa como `recebido`, e o worker o muda para `processado` (ou `erro`) depois de tentar salvar o JSON no S3.

Exemplo de corpo para o `POST /livros`:

```json
{
  "id": "12345",
  "titulo": "LoremIpsum",
  "autor": "John Doe",
  "ano": 1960,
  "genero": "romance",
  "resumo": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
}
```
```

### Como rodar

Na raiz do repositório:

```shell
docker compose up --build
```

### Testes e Ruff

```shell
uv run pytest
uv run ruff check .
```

## Arquitetura (Exercício 04)

```mermaid
flowchart LR
    C[Cliente] -->|POST /livros| A[API]
    A -->|envia livro| Q1[[livros-entrada.fifo]]
    Q1 -->|long polling| W[Worker]
    W -->|salva JSON| S3[(bucket do gênero)]
    W -->|avisa| Q2[[livros-saida.fifo]]
```

O worker lê a fila de entrada, salva o livro como `<titulo>.json` no bucket do gênero (`romance`, `ficcao` ou `outros`) e avisa na fila de saída. Os logs dele aparecem com `docker compose logs -f worker`.

## Arquitetura (Exercício 05)

```mermaid
flowchart LR
    C[Cliente] -->|POST /livros| A[API]
    A -->|status: recebido| DB[(PostgreSQL)]
    A -->|envia livro| Q1[[livros-entrada.fifo]]
    Q1 -->|long polling| W[Worker]
    W -->|salva JSON| S3[(bucket do gênero)]
    W -->|avisa| Q2[[livros-saida.fifo]]
    W -->|status: processado| DB
    C -->|GET /livros e /livros/id| A
```

A API grava cada livro com `status = recebido` antes de enviá-lo para a fila. O worker, depois de salvar o JSON no S3, atualiza o livro para `processado` (ou `erro`, se algo falhar). O cliente consulta o andamento com `GET /livros/{id}` e lista com `GET /livros?status=processado`.