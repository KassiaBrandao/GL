from fastapi import FastAPI
from app.database import engine, Base
from app.routers import dramas
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GL Drama API",
    description="API para gerenciar dramas do gênero GL (Girls Love).",
    version="1.0.0",
)

app.include_router(dramas.router, prefix="/dramas", tags=["dramas"])
