# :wave: Introdução

Olá, no projeto ToT - Text Of Things você terá uma experiência mais próxima à realidade do mercado de trabalho, utilizando tecnologias atuais adotadas por gigantes da tecnologia, terá a oportunidade de trabalhar com uma stack atual baseada em microsserviços, robusta e de alta escalabilidade.

Este README reúne tudo que você precisa para começar. Ele serve como um guia inicial para explorar as tecnologias utilizadas.

> Para melhor aproveitamento do conteúdo deve-se lêr a documentação da ferramenta, implementar exemplos, realizar as atividades sugeridas em cada tópico deste documento e só após recorrer a vídeos no YouTube para fixar o conteúdo.

**Ao fim do mesmo contem um exercício que deve ser implementado, utilizando parte dos conceitos apresentados neste documento.**

 
# :books: Conceitos básicos

1. Editor de Texto -> [VSCode](https://code.visualstudio.com/)
2. Windows com WSL (Ou Linux)-> [Win10/Win11 com WSL](https://docs.microsoft.com/pt-br/windows/wsl/install-win10)
3. Linguagem de Programação -> [Python 3.8.6 (minimo)](https://www.python.org/downloads/release/python-386/)
4. Versionamento -> [GIT](https://git-scm.com/downloads) e [SemVer - Versionamento Semântico](https://semver.org/)
5. Conteinerização -> [Docker](https://www.docker.com/), [dockerHUB](https://hub.docker.com/)
6. Processamento de Imagens -> [OCR - TesseractOCR V4.1.1 ou superior](https://github.com/tesseract-ocr/tesseract), [OpenCV](https://opencv.org/)
7. Desenvolvendo API'S -> [Flask](https://flask.palletsprojects.com/en/1.1.x/)
8. Ambiente núvem AWS -> [AWS](https://aws.amazon.com/)
9. SDK AWS python -> [Boto3](boto3.amazonaws.com/v1/documentation/api/latest/index.html)
10. Ambiente de emulação núvem -> [LocalStack](https://www.localstack.cloud/)
11. Uso de IA (Ollama ou Llama.cpp)


# :zap: Roadmap
Basta seguir o passo a passo para realização da atividade final.

## :computer: Configuração do Ambiente 
1.  OS Win10 com WSL - [Windows Subsystem Linux - WSL](https://docs.microsoft.com/pt-br/windows/wsl/install-win10)
   * > Caso não possua Hyper-V opte por trabalhar com WSL, pois o desempenho do docker será melhor.
   * > Realize a configuração para restrição de uso de recursos pelo WSL (memoria ram). [.wslconfig](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)
  
2. Editor de Texto -  [Instalaçao do VSCode](https://code.visualstudio.com/)
   * Pluggins Sugeridos:
     * [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
     * [MaterialIcons](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)
     * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
     * Remote Package:
       * [Remote WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
       * [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
       * [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   * > VSCode é sugerido como opção por facilitar o desenvolvimento integrando diversas ferramentas utilizadas no projeto.
 
3. Instalar Python
   * [Python 3.8.6](https://www.python.org/downloads/release/python-386/)
   * Atividades sugeridas:
     * aprender sobre ambientes virtuais [(virtualenv, venv)](https://docs.python.org/3/library/venv.html).
   * > Versão 3.8.6 ou maior, devido a compatibilidade com certas bibliotecas que o sistema utiliza.
  
4. Instalar Docker
   * [Docker](https://docs.docker.com/docker-for-windows/install/)

5. Instalar LocalStack
   * [Localstack](https://docs.localstack.cloud/getting-started/installation/)


## :hammer: Materiais e Ferramentas

1. Noções básicas do git/github
   * [Conta no Github](https://github.com/)
   * [Tutorial Basico - Introdução ao Git](https://www.hostinger.com.br/tutoriais/tutorial-do-git-basics-introducao)
   * [Introdução ao github](https://docs.github.com/pt/github/getting-started-with-github)
   * Atividades:
     * Instalar git (Sugiro adicionar ao menu de contexto do windows).
     * Criar conta github.
     * [Praticar o básico](https://learngitbranching.js.org/?locale=pt_BR)
  
2. Versionamento Semantico
   * [SemVer - Versionamento Semântico](https://semver.org/)
   * [Versionamento de Software](https://en.wikipedia.org/wiki/Software_versioning)
   * > Como qualquer projeto de desenvolvimento de software deve-se manter uma boa padronização e controle do versionamento.

3. Processamento de Imagens: 
   * [OCR - Visão Geral](https://en.wikipedia.org/wiki/Optical_character_recognition)
   * [TesseractOCR V4.1.1 ou Superior](https://github.com/tesseract-ocr/tesseract)
   * [Pytesseract](https://pypi.org/project/pytesseract/)
   * Atividades:
     * Instalar
     * Executar OCR em alguma imagem.
     * [Tutorial - Using Tesseract OCR with Python](https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/)

   * [OpenCV](https://opencv.org/)
   * [Python-OpenCV](https://pypi.org/project/opencv-python/)
   * Atividades:
     * Instalar
     * [Testar exemplos da documentação para Python](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
   * Bônus
     * [Tutorial - A comprehensive guide to OCR with Tesseract, OpenCV and Python](https://nanonets.com/blog/ocr-with-tesseract/)

4. Estudo de serviços AWS
   * Mensageria: SQS, SNS
   * FaaS: Lambda
   * Storage: S3
   * Containers: ECS, Fargate
   * Misc: ALB, Opensearch

5. SDK AWS para python:
   * Documentação [Boto3](boto3.amazonaws.com/v1/documentation/api/latest/index.html)



# :pencil: Exercício final

Desenvolva uma aplicação com Python + Flask + Docker que simula o seguinte fluxo completo, integrando serviços da AWS via LocalStack:
   1. Um cliente (via API) envia uma imagem .png para o bucket `image-input` no S3.
   2. A aplicação envia uma mensagem para a fila `new-image-input` no SQS, notificando que há uma nova imagem.
   3. Um container Flask (worker) roda em segundo plano fazendo o polling da fila SQS:
      * Quando detecta uma nova mensagem, busca a imagem do bucket S3 `image-input`
      * Processa a imagem com OpenCV (ex: binarização)
      * Salva a imagem tratada no bucket S3 `image-processed`
      * Envia uma nova mensagem para a fila `new-image-processed`, informando que a imagem foi processada com sucesso.


## Entregáveis

Para que sua entrega seja considerada completa, você deve incluir:

   * API Flask funcional com endpoint POST /upload para envio de imagem, rota de healthcheck e worker process
   * Integração com AWS (via LocalStack):
      * Upload da imagem no bucket `image-input` (S3)
      * Envio de mensagem para a fila `new-image-processed` (SQS)
   
   * Worker Flask:
      * Consome mensagens da fila ocr-events
      * Processa a imagem com OpenCV
      * Salva resultado no bucket output (S3)
      * Publica mensagem final na fila ocr-processed (SQS)

   * Estrutura dockerizada com docker-compose
   * Buckets e filas criadas no startup do container (pode ser via entrypoint.sh, init.py ou script Makefile)
   * Documentação da API com Swagger (OpenAPI 3.0):
      * Inclua a especificação no formato YAML ou JSON, ou useflask-restx ou apispec para gerar automaticamente
         * Documente ao menos:
         * Endpoint /upload
         * Campos do multipart/form-data
         * Códigos de resposta

   * README do repositório com instruções para execução local, incluindo:
      * Como subir os containers
      * Como testar a API
      * Como visualizar a documentação Swagger

   * Testes unitários e/ou de integração para os principais componentes:
      * Upload de imagem na API
      * Publicação e consumo da fila
      * Processamento de imagem
      * Upload no bucket de saída
      >💡 Sugestão: use pytest para testes e flask-testing para facilitar simulações de requisições à API.

**OBS:** Durante todo o processo utilize o github, crie um repositório e use versionamento semântico para organizar o trabalho.


### Dicas:
* Ao criar o github, gere um README e adicione a tag de versionamento inicial como V0.1.0 ao repositório.
* Podem haver alguns problemas ao conectar no minio pela API do python, basta encontrar qual IP sua maquina mapeou para acessar os containers do docker (normalmente pode ser IP WSL, IP da maquina local).
* Insira uma imagem de teste no formato png no bucket de entrada (input).
* Anotar e Relatar as principais dificuldades ao realizar as atividades.

    
