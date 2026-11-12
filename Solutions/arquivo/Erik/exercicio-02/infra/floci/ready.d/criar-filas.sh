#!/bin/sh
set -eu
aws --profile floci sqs create-queue --queue-name InputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false
aws --profile floci sqs create-queue --queue-name OutputQueue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=false