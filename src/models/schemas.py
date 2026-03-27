from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class TaskModel(Base):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    completed_ad: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[bool] = mapped_column(Boolean)
