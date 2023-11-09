FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "app:app", "-b", "0.0.0.0:5000", "--access-logfile=-"]