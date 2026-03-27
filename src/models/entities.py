import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class Task:
    id: uuid.UUID
    name: str
    details: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    status: bool


class AbstractRepo[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> None:
        raise NotImplementedError


class TaskRepo(AbstractRepo[Task]):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
