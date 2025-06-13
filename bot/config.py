from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    openweather_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
