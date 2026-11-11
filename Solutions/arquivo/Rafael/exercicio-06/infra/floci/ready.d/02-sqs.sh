#!/bin/sh
set -eu

aws sqs create-queue \
  --queue-name new-image-input.fifo \
  --attributes FifoQueue=true

aws sqs create-queue \
  --queue-name new-image-processed.fifo \
  --attributes FifoQueue=true
