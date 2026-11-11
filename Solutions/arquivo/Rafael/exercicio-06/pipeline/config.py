from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    aws_endpoint_url: str = "http://localhost:4566"
    aws_region: str = "us-east-1"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    input_bucket: str = "image-input"
    output_bucket: str = "image-output"
    input_queue: str = "new-image-input.fifo"
    processed_queue: str = "new-image-processed.fifo"


def get_settings() -> Settings:
    return Settings()
