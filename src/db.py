from typing import AsyncGenerator
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from platformdirs import user_data_dir

from src.models.schemas import Base


APP_NAME: str = "dutyy"


def _get_db_uri() -> str:
    data_dir: Path = Path(user_data_dir(appname=APP_NAME))
    data_dir.mkdir(parents=True, exist_ok=True)
    path: Path = data_dir / "database.db"
    return f"sqlite+aiosqlite:///{path}"


def _create_db_engine(db_uri: str) -> AsyncEngine:
    connect_args: dict[str, bool] = {"check_same_thread": False}
    return create_async_engine(url=db_uri, connect_args=connect_args)


db_uri: str = _get_db_uri()
engine: AsyncEngine = _create_db_engine(db_uri=db_uri)
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
