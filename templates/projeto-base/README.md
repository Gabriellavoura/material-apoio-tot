# Projeto base

Ponto de partida para os exercícios da trilha. Com um comando você sobe:

| Serviço | Endereço | Para quê |
|---------|----------|----------|
| API (FastAPI) | http://localhost:8000/docs | Sua aplicação |
| Floci | http://localhost:4566 | AWS local (S3, SQS) |
| floci-ui | http://localhost:4500 | Ver buckets e filas |
| PostgreSQL | `localhost:5432` | Banco de dados |
| CloudBeaver | http://localhost:8978 | Ver o banco (login `cbadmin` / `Tot12345`) |

## Como usar

1. Copie esta pasta para um repositório novo seu.
2. (Opcional) Copie `.env.example` para `.env` e troque as senhas.
3. Suba tudo:

   ```shell
   docker compose up --build
   ```

4. Teste: abra http://localhost:8000/health/deps. A resposta mostra que a API está falando com o Postgres e com o Floci.

## Estrutura

```
projeto-base/
├── app/
│   ├── main.py             # rotas da API
│   └── config.py           # configurações lidas do ambiente
├── tests/
│   └── test_health.py      # exemplo de teste
├── infra/
│   ├── floci/ready.d/      # scripts que criam buckets e filas quando o Floci sobe
│   └── cloudbeaver/        # conexão com o Postgres já cadastrada no CloudBeaver
├── compose.yaml            # todos os serviços
├── Dockerfile              # imagem da API
├── pyproject.toml          # dependências (gerenciadas com uv)
└── uv.lock                 # versões exatas das dependências (não edite à mão)
```

## Comandos úteis

| Comando | O que faz |
|---------|-----------|
| `docker compose up --build` | Sobe tudo, reconstruindo a imagem da API |
| `docker compose down` | Para tudo (os dados do banco são mantidos) |
| `docker compose down -v` | Para tudo e **apaga** os dados do banco e do CloudBeaver |
| `docker compose logs -f api` | Mostra os logs da API |
| `uv sync` | Instala as dependências no seu computador (para o VSCode reconhecer) |
| `uv add <pacote>` | Adiciona uma dependência |
| `uv run pytest` | Roda os testes |
| `uv run ruff check .` | Procura problemas no código |
| `uv run ruff format .` | Formata o código |

> Depois de `uv add`, rode `docker compose up --build` para a imagem receber o pacote novo.

## Versões usadas

Python 3.13 · uv 0.13.5 · Floci 2.3.0 · floci-ui 0.7.0 · PostgreSQL 18 · CloudBeaver 26.2.3. Testado em outubro de 2026.
