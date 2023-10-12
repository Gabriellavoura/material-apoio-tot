 ### Exercise 1: Setting Up S3 Buckets with LocalStack

**Objective:** Create two S3 buckets locally using LocalStack and AWS CLI with `awslocal`.

#### Prerequisites:

- Install Docker (if not already installed).
- Install AWS CLI (`awslocal`) using pip: `pip install awscli-local`

#### Instructions:

1. Start localstack in a docker container. Run the following command in your terminal:

   ```shell
   docker run -d -p 4566:4566 --name localstack-demo -e SERVICES=s3 localstack/localstack
   ```

2. Verify that localstack is up and running by visiting http://localhost:4566/health in your web browser or using `curl`:

    ```shell
    curl -v http://localhost:4566/health
    ```
    > You should see a response indicating that localstack is healthy.

3. Create the first S3 bucket locally. Use the AWS CLI (`awslocal`) to create a new S3 bucket. Replace <bucket-name-1> with a unique bucket name:

    ```shell
    awslocal s3 mb s3://<bucket-name-1>
    ```

4. Create the second S3 bucket.

    ```shell
    awslocal s3 mb s3://<bucket-name-2>
    ```

5. List the S3 buckets you've created locally using the following command:

    ```shell
    awslocal s3 ls
    ```
    > You should see a list of the two buckets you created.

### Cleanup:

To stop and remove the localstack container, run the following commands:

```shell
docker stop localstack-demo
docker rm localstack-demo
```

or remove it directly from the docker desktop interface.