import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    db_name: str = "emotion_db"
    collection_name: str = "predictions"
    model_dir: str = os.getenv("MODEL_DIR", "0712_kobert_5_emotion_model")
    title: str = "MovieMood - KoBERT Emotion API"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()