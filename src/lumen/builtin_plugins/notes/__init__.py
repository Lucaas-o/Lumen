from __future__ import annotations

import pluggy
from typing import TYPE_CHECKING

from lumen.core.hookspecs import SearchResult

if TYPE_CHECKING:
    import typer
    from lumen.core.context import AppContext

hookimpl = pluggy.HookimplMarker("lumen")


class NotesPlugin:
    @hookimpl
    def register_commands(self, cli: "typer.Typer") -> None:
        from lumen.cli.notes import notes_app
        cli.add_typer(notes_app, name="note")

    @hookimpl
    def on_startup(self, ctx: "AppContext") -> None:
        pass

    @hookimpl
    def get_search_results(self, query: str, ctx: "AppContext") -> list[SearchResult]:
        from lumen.storage.db import get_session
        from lumen.storage.repositories import NoteRepository

        repo = NoteRepository()
        with get_session(ctx.engine) as session:
            notes = repo.search(session, query)
        return [
            SearchResult(title=n.title, body=n.body[:100], source="notes")
            for n in notes
        ]