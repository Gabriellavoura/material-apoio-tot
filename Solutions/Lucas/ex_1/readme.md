# Aws s3 and sqs test project

This is a project that I did to practice aws sqs and s3 

## Folder structure

- **env.py**: set env variables to this file.
- **requirements.txt**: add application dependencies here.
- **localstack_setup.sh**: use this file to setup your localstack with the necessary aws services for local testing.
- **gunicorn_starter.sh**: this file has the command to start gunicorn; modify this file to change gunicorn starting settings.
- **app.py**: Entrypoint for the application; all the routes are defined here; add news routes here.
- **/src**: this folder has the source folder for the application; add necessary modules for the application here.
- **/handler**: this folder has the handlers of the routes in the app.py. Each route should have a handler file here responsible for handling requests. 

## How to run the application

- **Container building command**: `docker build -t myapplication:latest .`
- **Container running command**: `docker run -dit -p 5000:5000 myapplication *args`

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

 🚀