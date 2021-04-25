# Introdução
Olá, no projeto ToT - Text Of Things você terá uma experiência bem próxima do mercado de trabalho atual, tendo contato com diversas tecnologias utilizadas por gigantes da tecnologia, terá a oportunidade de trabalhar com uma stack atual baseada em microsserviços, robusta e de alta escalabilidade.
No grupo OCR você irá trabalhar com o desenvolvimento de ferramentas para o processamento de imagens e implementação das ferramentas desenvolvidas com os demais grupos do projeto.

Neste README você encontrará todas as informações necessárias para ter a primeira aproximação com as tecnologias utilizadas,
deve-se realizar, uma leitura basica dos links citados, acompanhado sempre que possível de testes com as ferramentas.

> OBS: Sugiro lêr a documentação da ferramenta, implementar exemplos, realizar as atividades sugeridas em cada tópico deste documento e só após recorrer a vídeos no YouTube para fixar o conteúdo.

**Ao fim do mesmo contem um exercício que deve ser implementado, utilizando parte dos conceitos apresentados neste documento.**

 
# :books: Conceitos básicos necessários

* Editor de Texto: 
  * [VSCode](https://code.visualstudio.com/)
  
* Sistema Operacional: 
  * [Win10/ WSL / Linux (Sugiro Win10 com WSL)](https://docs.microsoft.com/pt-br/windows/wsl/install-win10)
  
* Linguagem de Programação: 
  * [Python 3.8.6](https://www.python.org/downloads/release/python-386/)
  
* Versionamento:
  * [SemVer - Versionamento Semântico](https://semver.org/)
  * [GIT](https://git-scm.com/downloads)
  
* Conteinerização:
  * [Docker](https://www.docker.com/)
  * [Conta no dockerHUB](https://hub.docker.com/)
  * [Kubernets](https://kubernetes.io/pt-br/) ou [Minikube](https://minikube.sigs.k8s.io/) (Preferência do desenvolvedor) 

* Processamento de Imagens: 
  * [OCR - TesseractOCR V4.1.1 ou superior](https://github.com/tesseract-ocr/tesseract)
  * [OpenCV](https://opencv.org/)
    
* Function as a Services: 
  * [OpenFaaS](https://www.openfaas.com/)
  
* Desenvolvendo API'S: 
  * [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  
* Storage: 
  * [Min.io](https://min.io/)



# :zap: Roadmap sugerido

1. Editor de Texto
   * [Instalaçao do VSCode](https://code.visualstudio.com/)
   * Pluggins Sugeridos:
   * [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
   * [MaterialIcons](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)
   * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
   * Remote Package:
     * [Remote WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
     * [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
     * [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   * > VSCode é sugerido como opção por facilitar o desenvolvimento integrando diversas ferramentas utilizadas no projeto.

2. Instalar Python
   * [Python 3.8.6](https://www.python.org/downloads/release/python-386/)
   * Atividades sugeridas:
     * aprender sobre ambientes virtuais (virtualenv, venv).
   * > Versão 3.8.6 ou maior, devido a compatibilidade com certas bibliotecas que o sistema utiliza.
  
3. Noções básicas do git/github
   * [Conta no Github](https://github.com/)
   * [Tutorial Basico - Introdução ao Git](https://www.hostinger.com.br/tutoriais/tutorial-do-git-basics-introducao)
   * [Introdução ao github](https://docs.github.com/pt/github/getting-started-with-github)
   * Atividades:
     * Instalar git (Sugiro adicionar ao menu de contexto do windows).
     * Criar conta github.
     * [Praticar o básico](https://learngitbranching.js.org/?locale=pt_BR)
  
4. Versionamento Semantico
   * [SemVer - Versionamento Semântico](https://semver.org/)
   * [Versionamento de Software](https://en.wikipedia.org/wiki/Software_versioning)
   * > Como qualquer projeto de desenvolvimento de software deve-se manter uma boa padronização e controle do versionamento.

5. Processamento de Imagens: 
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
      * [Testar exemplos da documentação para Python](https://docs.opencv.org/master/d9/df8/tutorial_root.html).
  * Bônus
    * [Tutorial - A comprehensive guide to OCR with Tesseract, OpenCV and Python](https://nanonets.com/blog/ocr-with-tesseract/)
  
    
