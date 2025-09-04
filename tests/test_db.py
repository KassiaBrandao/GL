from sqlalchemy import create_engine, text
from app.core.config import settings

print("🔌 Testando conexão com o banco...")

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar_one()
        print("✅ Conectado com sucesso!")
        print("Versão do Postgres:", version)
except Exception as e:
    print("❌ Erro ao conectar:", e)
