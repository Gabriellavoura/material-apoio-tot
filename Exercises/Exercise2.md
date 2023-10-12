# Exercise 2: Setting Up FIFO SQS Queues with localStack

**Objective:** Create two FIFO SQS queues locally using localstack and AWS CLI (awslocal).

## Prerequisites:

* Docker is installed (if not already installed).
* AWS CLI and awslocal is installed (you can install it using pip: `pip install awscli-local`).

## Instructions:

1. Start localstack in a Docker container with SQS service enabled. Run the following command in your terminal:

    ```shell
    docker run -d -p 4566:4566 --name localstack-demo -e SERVICES=sqs localstack/localstack
    ```

2. Verify that localstack is up and running with SQS service enabled by visiting http://localhost:4566/health or using `curl`:

    ```shell
    curl -v http://localhost:4566/health
    ```
    > You should see a response indicating that localstack is healthy.

3. Create the first FIFO SQS queue locally. Use the `awslocal` to create an SQS FIFO queue named "InputQueue.fifo":

    ```shell
    awslocal sqs create-queue --queue-name InputQueue.fifo --attributes FifoQueue=true, ContentBasedDeduplication=false
    ```
    > Verify that the "InputQueue.fifo" is created successfully.

4. Create the second FIFO SQS queue locally. Use the `awslocal` to create another SQS FIFO queue named "OutputQueue.fifo":

    ```shell
    awslocal sqs create-queue --queue-name OutputQueue.fifo --attributes FifoQueue=true, ContentBasedDeduplication=false
    ```
    > Now OutputQueue.fifo" is also created successfully.

5. List the SQS queues you've created locally using the following command:

    ```shell
    awslocal sqs list-queues
    ```
    > You should see the "InputQueue.fifo" and "OutputQueue.fifo" in the list.


### Cleanup:

To stop and remove the localstack container, run the following commands:

```shell
docker stop localstack-demo
docker rm localstack-demo
```

or remove it directly from the docker desktop interface.