from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    API_V1_STR: str = "/api/v1"

    @property
    def DATABASE_URL(self) -> str:
        pwd = quote_plus(self.DB_PASSWORD)
        return f"postgresql+psycopg2://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
