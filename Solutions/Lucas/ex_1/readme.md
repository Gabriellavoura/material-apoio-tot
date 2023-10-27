# Aws s3 and sqs test project

This is a project that I did to practice aws sqs and s3 

## Routes

### 1. Initialization Route

- **Route**: `/`
- **Method**: POST
- **Description**: This route is used to initialize the listener.
- **Response**: N/A

### 2. Input Route

- **Route**: `/input`
- **Method**: POST
- **Description**: Use this route to input data into the QUEUE for the listener to process.
- **Response Codes**:
    - 200: Successful input
    - 400: Invalid data provided
    - 500: Server failure
- **Valid JSON Body Example**:
    ```json
    {
        "id": "12345",
        "title": "newtest",
        "author": "John Doe",
        "year": "1960",
        "genre": "scifi",
        "summary": "test"
    }
    ```
- **Requirements**:
    - No fields can be empty.
    - Genre must be "scifi" or "romance".
    - Title must be less than 230 characters.

### 3. Health Route

- **Route**: `/health`
- **Method**: GET
- **Description**: This route checks if the server is up and running.
- **Response Codes**:
    - 200: Server is up

## Observations

- To see log messages being printed, it's recommended to run the Docker container with the `-it` flag.

 🚀