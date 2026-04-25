
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    # SECURITY
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "af8ac01addbcf0df40a4a521b84aa9a6ae36ae5d17c238714f0cd69b5a6ac8ee"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()

