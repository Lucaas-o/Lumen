# src\lumen\cli\notes.py
from __future__ import annotations

from typing import Any

import typer
from rich.console import Console
from rich.table import Table

notes_app = typer.Typer(help="Gestiona tus notas.")
console = Console()


def _get_ctx(ctx: typer.Context) -> Any:
    return ctx.find_root().obj


@notes_app.command("add")
def note_add(
    ctx: typer.Context,
    title: str = typer.Argument(..., help="Título de la nota"),
    body: str = typer.Option("", "--body", "-b", help="Cuerpo de la nota"),
    tag: list[str] = typer.Option([], "--tag", "-t", help="Etiqueta (repetible)"),
) -> None:
    """Crea una nueva nota."""
    from lumen.storage.db import get_session
    from lumen.storage.repositories import NoteRepository

    app_ctx = _get_ctx(ctx)
    repo = NoteRepository()
    with get_session(app_ctx.engine) as session:
        note = repo.create(session, title=title, body=body, tags=tag)
    console.print(f"[green]✓[/green] Nota creada [dim](id: {note.id})[/dim]")


@notes_app.command("ls")
def note_ls(
    ctx: typer.Context,
    limit: int = typer.Option(20, "--limit", "-n"),
) -> None:
    """Lista las notas más recientes."""
    from lumen.storage.db import get_session
    from lumen.storage.repositories import NoteRepository

    app_ctx = _get_ctx(ctx)
    repo = NoteRepository()
    with get_session(app_ctx.engine) as session:
        notes = repo.list_recent(session, limit=limit)

    if not notes:
        console.print(
            '[dim]Sin notas todavía. Prueba: lumen note add "mi primera nota"[/dim]'
        )
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Título")
    table.add_column("Tags", style="dim")
    table.add_column("Creada", style="dim")

    for n in notes:
        table.add_row(
            str(n.id),
            n.title,
            ", ".join(n.get_tags()) or "—",
            n.created_at.strftime("%Y-%m-%d"),
        )
    console.print(table)


@notes_app.command("show")
def note_show(
    ctx: typer.Context,
    note_id: int = typer.Argument(..., help="ID de la nota"),
) -> None:
    """Muestra el contenido completo de una nota."""
    from rich.panel import Panel

    from lumen.storage.db import get_session
    from lumen.storage.repositories import NoteRepository

    app_ctx = _get_ctx(ctx)
    repo = NoteRepository()
    with get_session(app_ctx.engine) as session:
        note = repo.get(session, note_id)

    if not note:
        console.print(f"[red]Nota {note_id} no encontrada.[/red]")
        raise typer.Exit(1)

    console.print(Panel(note.body or "[dim]Sin contenido[/dim]", title=note.title))


@notes_app.command("delete")
def note_delete(
    ctx: typer.Context,
    note_id: int = typer.Argument(..., help="ID de la nota"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirmar sin preguntar"),
) -> None:
    """Elimina una nota."""
    from lumen.storage.db import get_session
    from lumen.storage.repositories import NoteRepository

    if not yes:
        typer.confirm(f"¿Eliminar nota {note_id}?", abort=True)

    app_ctx = _get_ctx(ctx)
    repo = NoteRepository()
    with get_session(app_ctx.engine) as session:
        ok = repo.delete(session, note_id)

    if ok:
        console.print(f"[green]✓[/green] Nota {note_id} eliminada.")
    else:
        console.print(f"[red]Nota {note_id} no encontrada.[/red]")
