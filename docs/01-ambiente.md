# 01 · Preparando o ambiente

Aqui você instala tudo o que precisa para trabalhar no ToT. Siga na ordem. Cada passo tem um teste para conferir se deu certo.

> **Sistema operacional:** use **Linux**, **macOS** ou **Windows com WSL 2**. No Windows, todos os comandos deste material são rodados **dentro do WSL** (no terminal do Ubuntu), não no PowerShell.

## 1. WSL 2 (somente Windows)

O WSL roda um Linux de verdade dentro do Windows. Assim o seu ambiente fica igual ao do resto da equipe.

- Instale o WSL com Ubuntu 24.04 seguindo a [documentação oficial](https://learn.microsoft.com/pt-br/windows/wsl/install). No PowerShell, como administrador:

  ```powershell
  wsl --install -d Ubuntu-24.04
  ```

- **Limite a memória que o WSL pode usar**, para o Windows não ficar lento. Crie o arquivo `C:\Users\<seu-usuario>\.wslconfig`. Veja a [doc de configuração do WSL](https://learn.microsoft.com/pt-br/windows/wsl/wsl-config):

  ```ini
  [wsl2]
  memory=8GB
  processors=4
  ```

- **Guarde seus projetos dentro do Linux** (por exemplo em `~/projetos`), não em `/mnt/c/...`. Fica bem mais rápido.

**Teste:** `wsl -l -v` no PowerShell mostra o Ubuntu com `VERSION 2`.

## 2. VSCode

Baixe o [VSCode](https://code.visualstudio.com/). No Windows, instale no Windows (não no WSL) e abra os projetos pelo WSL com o comando `code .` no terminal do Ubuntu.

Extensões recomendadas:

| Extensão | Para quê |
|----------|----------|
| [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) | Abrir projetos que estão dentro do WSL |
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) | Rodar e depurar código Python |
| [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) | Apontar erros e formatar o código Python |
| [Container Tools](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers) | Ver containers e arquivos Docker |
| [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) | Programar dentro de um container |
| [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) | Ver o histórico do Git direto no código |
| [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) | Assistente de IA (veja o [guia de IA](06-ia.md)) |

Documentação: [code.visualstudio.com/docs](https://code.visualstudio.com/docs) · [VSCode com WSL](https://code.visualstudio.com/docs/remote/wsl).

## 3. Git

O Git guarda o histórico do seu código. Instale seguindo a [página oficial](https://git-scm.com/downloads). No Ubuntu/WSL:

```shell
sudo apt update && sudo apt install -y git
```

Configure seu nome e e-mail (use o mesmo e-mail da sua conta do GitHub):

```shell
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
git config --global init.defaultBranch main
```

Para enviar código ao GitHub sem digitar senha, [configure uma chave SSH](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh).

**Teste:** `git --version` mostra a versão, e `ssh -T git@github.com` responde com o seu usuário.

## 4. Python com uv

O **uv** instala o Python e as bibliotecas do projeto. Ele substitui `pip`, `venv` e `pyenv` com uma ferramenta só, e é bem rápido. Siga a [instalação oficial](https://docs.astral.sh/uv/getting-started/installation/):

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Feche e abra o terminal. Depois instale o Python:

```shell
uv python install 3.13
```

Comandos que você vai usar sempre:

| Comando | O que faz |
|---------|-----------|
| `uv init meu-projeto` | Cria um projeto novo com `pyproject.toml` |
| `uv add fastapi` | Adiciona uma biblioteca ao projeto |
| `uv add --dev pytest` | Adiciona uma biblioteca usada só no desenvolvimento |
| `uv sync` | Instala tudo o que está no `pyproject.toml` |
| `uv run pytest` | Roda um comando usando o ambiente do projeto |

> Você não precisa ativar ambiente virtual: o `uv run` cuida disso. A pasta `.venv` é criada sozinha e **não** vai para o Git.

Documentação: [docs.astral.sh/uv](https://docs.astral.sh/uv/) · [Python](https://docs.python.org/pt-br/3/).

**Teste:** `uv --version` e `uv run --python 3.13 python --version`.

## 5. Docker

O Docker roda programas dentro de **containers**, pequenas "caixas" que já vêm com tudo configurado. É com ele que subimos o Floci, o PostgreSQL e a sua API.

- **Windows:** instale o [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) e ative a [integração com o WSL](https://docs.docker.com/desktop/features/wsl/).
- **macOS:** instale o [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/).
- **Linux:** instale o [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) e siga os [passos pós-instalação](https://docs.docker.com/engine/install/linux-postinstall/) para usar o Docker sem `sudo`.

O **Docker Compose** já vem junto. Com ele você sobe vários containers com um comando só, a partir do arquivo `compose.yaml`. Veja a [doc do Compose](https://docs.docker.com/compose/).

**Teste:**

```shell
docker run --rm hello-world
docker compose version
```

## 6. AWS CLI v2

A **AWS CLI** é a linha de comando da AWS. Nós a usamos para criar e conferir buckets e filas no Floci (o emulador da AWS que roda no seu computador). Instale a **versão 2** seguindo a [documentação oficial](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

Linux/WSL (processador x86_64):

```shell
sudo apt install -y unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
```

> Processador ARM (por exemplo, um Linux em Raspberry Pi) usa outro link. No macOS, use o instalador `.pkg`. Os dois estão na página oficial.

### Perfil `floci`

Crie um **perfil** para que a AWS CLI fale com o Floci em vez da AWS de verdade. No Floci, qualquer usuário e senha funcionam. Usamos `test`.

Adicione ao arquivo `~/.aws/config`:

```ini
[profile floci]
region = us-east-1
endpoint_url = http://localhost:4566
```

E ao arquivo `~/.aws/credentials`:

```ini
[floci]
aws_access_key_id = test
aws_secret_access_key = test
```

Agora é só acrescentar `--profile floci` aos comandos. Por exemplo, `aws --profile floci s3 ls`. Se preferir, ative o perfil no terminal atual com `export AWS_PROFILE=floci`.

> Você vai ver em tutoriais antigos o comando `awslocal`. Ele não é mais necessário: o perfil acima faz o mesmo papel.

Documentação: [arquivos de configuração](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) · [endpoint personalizado](https://docs.aws.amazon.com/sdkref/latest/guide/feature-ss-endpoints.html).

**Teste:** `aws --version` mostra `aws-cli/2.x`. O teste com o Floci fica para o [guia 03](03-aws-local-floci.md).

## 7. Teste final: rode o projeto base

```shell
git clone <url-deste-repositorio>
cd material-apoio-tot/templates/projeto-base
docker compose up --build
```

Abra no navegador:

- `http://localhost:8000/docs`: a sua API
- `http://localhost:4500`: o floci-ui (buckets e filas)
- `http://localhost:8978`: o CloudBeaver (banco de dados)

Se as três páginas abriram, seu ambiente está pronto. :tada:

Para parar, aperte `Ctrl+C` no terminal ou rode `docker compose down`.

## Problemas comuns

| Problema | Solução |
|----------|---------|
| `permission denied` ao usar `docker` no Linux | Faça os [passos pós-instalação](https://docs.docker.com/engine/install/linux-postinstall/) e abra um terminal novo |
| `port is already allocated` | Outro programa usa a porta. Pare o container antigo (`docker ps` e depois `docker stop <id>`) |
| WSL muito lento | Confira se o projeto está em `~/` e não em `/mnt/c/` |
| `docker` não funciona dentro do WSL | Ative a integração com o WSL no Docker Desktop: *Settings > Resources > WSL integration* |
