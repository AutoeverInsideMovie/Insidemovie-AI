# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_name: str = "emotion_db"
    mongodb_uri: str = "mongodb://localhost:27017"
    collection_name: str = "predictions"
    title: str = "Inside Movie AI"

    # .env 파일 자동 로딩 설정
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()