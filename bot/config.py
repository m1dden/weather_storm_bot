from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    openweather_api_key: str = Field(..., env="OPENWEATHER_API_KEY")
    admin_id: int = Field(default=0, env="ADMIN_ID")  # 0 - значение по умолчанию
    
    @validator('admin_id')
    def validate_admin_id(cls, v):
        if v == 0:
            raise ValueError("ADMIN_ID must be set in .env file")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"  # Игнорировать лишние переменные в .env

settings = Settings()
