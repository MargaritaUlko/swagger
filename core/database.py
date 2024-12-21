from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5433/app_db"

# Создание асинхронного подключения к базе данных
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создание фабрики асинхронных сессий
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция для получения асинхронной сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Базовый класс для моделей
Base = declarative_base()