FROM python:3.8.6

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "main:app", "-b", "0.0.0.0", "--access-logfile=-"]