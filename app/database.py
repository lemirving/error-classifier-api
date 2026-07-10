import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings # <-- Importa o nosso gerenciador de configs

DATABASE_URL = settings.DATABASE_URL

# Cria o motor assíncrono que vai gerenciar a comunicação com o PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Função geradora de sessões para usarmos nas nossas rotas do FastAPI
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session