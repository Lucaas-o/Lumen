# src\lumen\domain\note.py
from __future__ import annotations

import json
from datetime import datetime
from typing import cast

from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    body: str = Field(default="")
    tags: str = Field(default="[]")  # JSON list[str]
    pinned: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def get_tags(self) -> list[str]:
        return cast(list[str], json.loads(self.tags))

    def set_tags(self, tags: list[str]) -> None:
        self.tags = json.dumps(tags)
