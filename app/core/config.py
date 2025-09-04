from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # ATENÇÃO: Substitua '[YOUR-PASSWORD]' pela sua senha real do banco de dados.
    # É mais seguro usar variáveis de ambiente para isso em produção.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:[YOUR-PASSWORD]@db.podtxoestfoxscdqrlgi.supabase.co:5432/postgres")
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
