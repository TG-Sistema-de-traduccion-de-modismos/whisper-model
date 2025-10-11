from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "whisper-model"
    HOST: str = "0.0.0.0"
    PORT: int = 8004

    MODEL_NAME: str = "medium"  
    DEVICE: str = "cuda"         
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1

    REQUEST_TIMEOUT_SECONDS: int = 300

    class Config:
        env_file = ".env"

settings = Settings()
