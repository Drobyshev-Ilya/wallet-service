from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Используйте localhost при локальном запуске, db при запуске в Docker
host = "localhost" if os.environ.get("LOCAL_TEST") else "db"
DATABASE_URL = f"postgresql+asyncpg://postgres:12345678@{host}:5432/wallet_db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
