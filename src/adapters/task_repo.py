import uuid
from typing import Sequence

from dataclasses import asdict
from sqlalchemy import Select, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters._abstract_repo import AbstractRepo
from src.domain.entities import Task
from src.domain.enums import TaskStatus
from src.models.schemas import TaskModel

class TaskRepo(AbstractRepo[Task]):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_by_id(self, id: uuid.UUID) -> Task | None:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(TaskModel.id == id)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        model: TaskModel | None = result.scalar_one_or_none()
        if model is None:
            return None
        return Task(**model.to_dict())

    async def get_by_name(self, name: str) -> Task | None:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(TaskModel.name == name)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        model: TaskModel | None = result.scalar_one_or_none()
        if model is None:
            return None
        return Task(**model.to_dict())

    async def get_all(self) -> list[Task]:
        stmt: Select[tuple[TaskModel]] = select(TaskModel)
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        models: Sequence[TaskModel] = result.scalars().all()
        return [Task(**model.to_dict()) for model in models]

    async def get_all_incomplete(self) -> list[Task]:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(
            TaskModel.status == "incomplete"
        )
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        models: Sequence[TaskModel] = result.scalars().all()
        return [Task(**model.to_dict()) for model in models]

    async def add(self, entity: Task) -> None:
        model: TaskModel = TaskModel(**asdict(entity))
        self.session.add(model)

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

    async def search_by_name(self, name: str) -> list[Task]:
        stmt: Select[tuple[TaskModel]] = select(TaskModel).where(
            TaskModel.name.like(f"%{name}%"), TaskModel.status == TaskStatus.INCOMPLETE
        )
        result: Result[tuple[TaskModel]] = await self.session.execute(stmt)
        models: Sequence[TaskModel] = result.scalars().all()
        return [Task(**model.to_dict()) for model in models]
