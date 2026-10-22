# 04 · Banco de dados: PostgreSQL e CloudBeaver

Arquivos (como imagens) ficam no S3. Já as **informações sobre** esses arquivos ficam em um **banco de dados**: nome, status, quando chegou, quando terminou. Usamos o **PostgreSQL**.

- [Documentação do PostgreSQL 18](https://www.postgresql.org/docs/18/) · [Tutorial oficial](https://www.postgresql.org/docs/18/tutorial.html)
- [Imagem oficial no Docker Hub](https://hub.docker.com/_/postgres)

## O que é um banco relacional

Pense em uma planilha bem organizada:

- uma **tabela** é como uma aba da planilha (por exemplo, `imagens`);
- cada **coluna** é um tipo de informação (`id`, `nome`, `status`);
- cada **linha** é um registro (uma imagem).

| id | nome | status | criada_em |
|----|------|--------|-----------|
| 1 | nota-fiscal.png | processada | 2026-10-22 10:00 |
| 2 | recibo.png | pendente | 2026-10-22 10:05 |

Para conversar com o banco usamos a linguagem **SQL**.

## Subindo o PostgreSQL e o CloudBeaver

O **CloudBeaver** é a versão web do [DBeaver](https://dbeaver.io/), feita pela mesma empresa. Ele abre no navegador e mostra as tabelas e os dados, e também permite rodar SQL. Documentação: [CloudBeaver](https://dbeaver.com/docs/cloudbeaver/).

O [projeto base](../templates/projeto-base/) já sobe os dois. O trecho do `compose.yaml` é este:

```yaml
  postgres:
    image: postgres:18
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: tot
      POSTGRES_PASSWORD: tot
      POSTGRES_DB: vddb
    volumes:
      - pgdata:/var/lib/postgresql   # guarda os dados mesmo se o container for recriado

  cloudbeaver:
    image: dbeaver/cloudbeaver:26.2.3
    ports:
      - "8978:8978"
    environment:
      CB_SERVER_NAME: ToT
      CB_ADMIN_NAME: cbadmin
      CB_ADMIN_PASSWORD: Tot12345
    volumes:
      - ./infra/cloudbeaver/data-sources.json:/opt/cloudbeaver/conf/initial-data-sources.conf:ro
      - cloudbeaver:/opt/cloudbeaver/workspace
```

> As senhas acima servem **só para uso local**. Em qualquer servidor de verdade, use senhas fortes guardadas fora do Git.

### Acessando o banco

1. Abra `http://localhost:8978`.
2. Clique em **Login** e entre com `cbadmin` / `Tot12345`.
3. A conexão **vddb (Postgres local)** já aparece cadastrada. Clique nela para ver as tabelas.
4. Para escrever SQL, abra o **SQL Editor** (ícone `SQL` no topo).

Prefere um programa instalado? Baixe o [DBeaver Community](https://dbeaver.io/download/) e crie uma conexão PostgreSQL com host `localhost`, porta `5432`, banco `vddb`, usuário `tot` e senha `tot`.

> **Dentro** do Compose, o endereço do banco é `postgres` (o nome do serviço). **Fora** dele, como no DBeaver instalado no seu computador, o endereço é `localhost`.

## SQL básico

Rode no SQL Editor do CloudBeaver:

```sql
-- cria a tabela
CREATE TABLE imagens (
    id        SERIAL PRIMARY KEY,
    nome      TEXT NOT NULL,
    status    TEXT NOT NULL DEFAULT 'pendente',
    criada_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- insere linhas
INSERT INTO imagens (nome) VALUES ('nota-fiscal.png'), ('recibo.png');

-- consulta
SELECT * FROM imagens WHERE status = 'pendente';

-- atualiza
UPDATE imagens SET status = 'processada' WHERE id = 1;

-- apaga
DELETE FROM imagens WHERE id = 2;
```

Saiba mais nos capítulos [SQL Language](https://www.postgresql.org/docs/18/tutorial-sql.html) do tutorial oficial.

## Usando no Python

Seguimos o [tutorial de banco de dados do FastAPI](https://fastapi.tiangolo.com/pt/tutorial/sql-databases/). Ele usa o **SQLModel**, que permite escrever a tabela como uma classe Python, sem SQL na mão. Por baixo, o driver **psycopg** faz a conexão com o PostgreSQL.

```shell
uv add sqlmodel "psycopg[binary]"
```

```python
from datetime import datetime, timezone

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Imagem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    status: str = "pendente"
    criada_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


engine = create_engine("postgresql+psycopg://tot:tot@localhost:5432/vddb")
SQLModel.metadata.create_all(engine)  # cria as tabelas que ainda não existem

with Session(engine) as session:
    session.add(Imagem(nome="nota-fiscal.png"))
    session.commit()

    pendentes = session.exec(select(Imagem).where(Imagem.status == "pendente")).all()
    print(pendentes)
```

Documentação: [SQLModel](https://sqlmodel.tiangolo.com/) · [psycopg 3](https://www.psycopg.org/psycopg3/docs/).

## Atividades

- [ ] Subir o projeto base e entrar no CloudBeaver.
- [ ] Rodar os comandos do "SQL básico" e ver o resultado na tela.
- [ ] Fazer o [Exercício 05: banco de dados](../Exercises/05-banco-de-dados.md).
