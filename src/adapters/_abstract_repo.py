import uuid
from abc import ABC, abstractmethod


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
