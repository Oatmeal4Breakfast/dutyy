import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Sequence
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select, Result
from src.models.schemas import TaskModel, TaskStatus


@dataclass
class Task:
    id: uuid.UUID
    name: str
    created_at: datetime
    status: TaskStatus
    completed_at: Optional[datetime] = None
    details: Optional[str] = None


def _to_entity(model: TaskModel) -> Task:
    return Task(
        id=model.id,
        name=model.name,
        details=model.details,
        created_at=model.created_at,
        completed_at=model.completed_at,
        status=model.status,
    )


def _to_model(entity: Task) -> TaskModel:
    return TaskModel(
        name=entity.name,
        details=entity.details,
        created_at=entity.created_at,
        completed_at=entity.completed_at,
        status=entity.status,
        id=entity.id,
    )


class AbstractRepo[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> None:
        raise NotImplementedError


class TaskRepo(AbstractRepo[Task]):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_by_id(self, id: uuid.UUID) -> Task | None:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(TaskModel.id == id)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        model: TaskModel | None = result.scalar_one_or_none()
        if model is None:
            return None
        return _to_entity(model)

    async def get_by_name(self, name: str) -> Task | None:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(TaskModel.name == name)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        model: TaskModel | None = result.scalar_one_or_none()
        if model is None:
            return None
        return _to_entity(model)

    async def get_all(self) -> list[Task]:
        stmt: Select[tuple[TaskModel]] = select(TaskModel)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        models: Sequence[TaskModel] = result.scalars().all()
        return [_to_entity(model) for model in models]

    async def get_all_incomplete(self) -> list[Task]:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(
            TaskModel.status == "incomplete"
        )
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        models: Sequence[TaskModel] = result.scalars().all()
        return [_to_entity(model) for model in models]

    async def add(self, entity: Task) -> None:
        model: TaskModel = _to_model(entity)
        self.session.add((model))

    async def update(self, entity: Task) -> Task | None:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(
            TaskModel.id == entity.id
        )
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        model: TaskModel | None = result.scalar_one_or_none()
        if model is None:
            return
        for key, value in asdict(entity).items():
            if key != "id":
                setattr(model, key, value)
        return entity
