FROM python:3.8.6

WORKDIR /app

COPY . .

# Install requirements
RUN pip install -r requirements.txt
RUN chmod +x /app/gunicorn_starter.sh

# Http server running on this port
EXPOSE 5000

ENTRYPOINT ["./gunicorn_starter.sh"]
