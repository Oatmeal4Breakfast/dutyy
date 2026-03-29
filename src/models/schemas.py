from sqlalchemy import String, DateTime, types, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from uuid import UUID
from enum import StrEnum, auto
from typing import Optional


class TaskStatus(StrEnum):
    COMPLETE = auto()
    INCOMPLETE = auto()


class Base(DeclarativeBase):
    pass


class TaskModel(Base):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
    )

    id: Mapped[UUID] = mapped_column(types.UUID, primary_key=True)
