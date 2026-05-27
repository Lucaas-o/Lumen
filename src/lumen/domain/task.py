# src\lumen\domain\task.py
from __future__ import annotations

import json
from datetime import date, datetime
from enum import IntEnum
from typing import cast

from sqlmodel import Field, SQLModel


class Priority(IntEnum):
    NORMAL = 0
    HIGH = 1
    URGENT = 2


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    done: bool = Field(default=False)
    due_date: date | None = Field(default=None)
    priority: int = Field(default=Priority.NORMAL)
    tags: str = Field(default="[]")  # JSON list[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    done_at: datetime | None = Field(default=None)

    def get_tags(self) -> list[str]:
        return cast(list[str], json.loads(self.tags))
