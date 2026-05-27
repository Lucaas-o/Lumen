from __future__ import annotations

import pluggy
from typing import TYPE_CHECKING

from lumen.core.hookspecs import SearchResult

if TYPE_CHECKING:
    import typer
    from lumen.core.context import AppContext

hookimpl = pluggy.HookimplMarker("lumen")


class TasksPlugin:
    @hookimpl
    def register_commands(self, cli: "typer.Typer") -> None:
        from lumen.cli.tasks import tasks_app
        cli.add_typer(tasks_app, name="task")

    @hookimpl
    def on_startup(self, ctx: "AppContext") -> None:
        pass

    @hookimpl
    def get_search_results(self, query: str, ctx: "AppContext") -> list[SearchResult]:
        from sqlmodel import select
        from lumen.storage.db import get_session
        from lumen.domain.task import Task

        results = []
        with get_session(ctx.engine) as session:
            tasks = session.exec(
                select(Task).where(Task.title.like(f"%{query}%"))
            ).all()
        return [
            SearchResult(title=t.title, body="", source="tasks")
            for t in tasks
        ]