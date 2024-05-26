from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    PAGE_SIZE: int = 10
    DATABASE_URL: str = "sqlite:///./app.db"


app_settings = AppSettings()
