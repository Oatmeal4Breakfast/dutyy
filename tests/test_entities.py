import pytest
import uuid
from dataclasses import asdict

from src.models.entities import AbstractRepo, Task


class FakeTaskRepo(AbstractRepo[Task]):
    def __init__(self) -> None:
        self._tasks: dict[uuid.UUID, Task] = {}

    async def get_by_id(self, id: uuid.UUID) -> Task | None:
        return self._tasks.get(id)

    async def get_by_name(self, name: str) -> Task | None:
        for key, value in self._tasks.items():
            if value.name == name:
                return self._tasks.get(key)

    async def add(self, entity) -> None:
        self._tasks[entity.id] = entity
        return

    async def update(self, entity) -> None:
        stored_ent = self._tasks.get(entity.id)
        if stored_ent is None:
            return
        for key, value in asdict(entity).items():
            if key != "id":
                setattr(stored_ent, key, value)
