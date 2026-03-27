from typing import AsyncGenerator
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from src.models.schemas import Base
from src.config import Config, get_config

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _build_db_uri(config: Config) -> str:
    if config.db_uri.startswith("sqlite:///"):
        db_file_path: str = config.db_uri.replace("sqlite:///", "")
        db_abs_path: Path = PROJECT_ROOT / db_file_path
        db_abs_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_abs_path}"
    else:
        raise ValueError(f"{config.db_uri} is not a valid sqlite uri")


def _create_db_engine(db_uri: str) -> AsyncEngine:
    connect_args: dict[str, bool] = {"check_same_thread": False}
    return create_async_engine(url=db_uri, connect_args=connect_args)


config: Config = get_config()
db_uri: str = _build_db_uri(config=config)
engine: AsyncEngine = _create_db_engine(db_uri=db_uri)
SessonLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessonLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
