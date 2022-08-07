from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    DB_URI: str = ""
    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None
    REDIS_DB: int | None = None
    

@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
