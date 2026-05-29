import uuid
from datetime import datetime
from dataclasses import dataclass, asdict, field
from src.domain.enums import TaskStatus


@dataclass
class Task:
    name: str
    created_at: datetime
    status: TaskStatus
    completed_at: datetime | None = None
    details: str | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid7)
