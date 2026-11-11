#!/bin/sh
set -eu
aws sqs create-queue --queue-name livros-entrada.fifo --attributes FifoQueue=true
