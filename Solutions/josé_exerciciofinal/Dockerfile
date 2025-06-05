FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Instalar dependências do sistema necessárias para o OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Atualizar pip e instalar dependências Python
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

# Definindo o comando para rodar a API
CMD ["flask", "run", "--host=0.0.0.0"]
