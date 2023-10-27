FROM python:3.8

WORKDIR /app

COPY . .

# Install requirements
RUN pip install -r requirements.txt
RUN chmod +x /app/gunicorn_starter.sh

# Flask http server running on this port
EXPOSE 5000

ENTRYPOINT ["/app/gunicorn_starter.sh"]

# Running flask HTTP server
#CMD ["flask", "run", "--host", "0.0.0.0"]
#CMD ["python", "app.py"]