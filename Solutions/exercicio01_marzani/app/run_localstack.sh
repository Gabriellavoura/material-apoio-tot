#!/bin/sh

# Sets the localstack settings
export AWS_ACCOUNT_ID="test"
export AWS_PROFILE="localstack"


# Create the queues using awslocal
echo "Creating the queues ..."
awslocal sqs create-queue --queue-name InputQueue.fifo --attributes FifoQueue=true
awslocal sqs create-queue --queue-name OutputQueue.fifo --attributes FifoQueue=true


# Create the buckets
echo "Creating buckets ..."
awslocal s3api create-bucket --bucket scifi
awslocal s3api create-bucket --bucket romance


# Sends a message to the pdf-new queue
echo "Sending a message to the InputQueue..."
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "test" --message-deduplication-id "test" --message-body '{"id": "1452345", "title":"Testando", "author": "John Doe", "year":"1960", "genre":"scifi", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}'

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "testioaop" --message-deduplication-id "testioaop" --message-body '{"id": "1234567", "title":"LoremIpsumDolors", "author": "John Doe", "year":"1960", "genre":"romance", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua de la Muerte."}'

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "salvarnobucket" --message-deduplication-id "salvarnobucket" --message-body '{"id": "444444", "title":"Salvandonobucket", "author": "Marzani", "year":"1960", "genre":"scifi", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua de la Muerte."}'

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "salvarnobucket" --message-deduplication-id "salvarnobucket" --message-body '{"id": "444444", "title":"Salvandonobucket", "author": "Marzani", "year":"1960", "genre":"scifi", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua de la Muerte."}'

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "testefinal" --message-deduplication-id "testefinal" --message-body '{"id": "12", "title":"teste_final", "author": "Marzani", "year":"1960", "genre":"romance", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua de la Muerte."}'
