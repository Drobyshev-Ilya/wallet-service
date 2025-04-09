from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from .routes import wallet

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Обработчик событий продолжительности жизни для приложения FastAPI."""
    try:
        # Запуск: Создание таблиц базы данных
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        # Завершение работы: Уничтожение движка
        await engine.dispose()

app = FastAPI(
    title="Wallet Service",
    description="A simple wallet service with FastAPI",
    lifespan=lifespan
)

app.include_router(wallet.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
