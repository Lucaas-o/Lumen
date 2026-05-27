# src\lumen\cli\tasks.py
from __future__ import annotations

from typing import Any

import typer
from rich.console import Console
from rich.table import Table

tasks_app = typer.Typer(help="Gestiona tus tareas.")
console = Console()


def _get_ctx(ctx: typer.Context) -> Any:
    return ctx.find_root().obj


@tasks_app.command("add")
def task_add(
    ctx: typer.Context,
    title: str = typer.Argument(..., help="Título de la tarea"),
    due: str = typer.Option(None, "--due", "-d", help="Fecha límite (YYYY-MM-DD)"),
    priority: str = typer.Option(
        "normal", "--priority", "-p", help="normal | high | urgent"
    ),
) -> None:
    """Crea una nueva tarea."""
    from datetime import date

    from lumen.domain.task import Priority
    from lumen.storage.db import get_session
    from lumen.storage.repositories import TaskRepository

    pmap = {
        "normal": Priority.NORMAL,
        "high": Priority.HIGH,
        "urgent": Priority.URGENT,
    }
    prio = pmap.get(priority, Priority.NORMAL)
    due_date = date.fromisoformat(due) if due else None

    app_ctx = _get_ctx(ctx)
    repo = TaskRepository()
    with get_session(app_ctx.engine) as session:
        task = repo.create(session, title=title, due_date=due_date, priority=prio)
    console.print(f"[green]✓[/green] Tarea creada [dim](id: {task.id})[/dim]")


@tasks_app.command("ls")
def task_ls(
    ctx: typer.Context,
    all: bool = typer.Option(False, "--all", "-a", help="Mostrar también completadas"),
    limit: int = typer.Option(50, "--limit", "-n"),
) -> None:
    """Lista tareas pendientes."""
    from lumen.domain.task import Priority
    from lumen.storage.db import get_session
    from lumen.storage.repositories import TaskRepository

    app_ctx = _get_ctx(ctx)
    repo = TaskRepository()

    pcolor = {Priority.NORMAL: "white", Priority.HIGH: "yellow", Priority.URGENT: "red"}
    plabel = {
        Priority.NORMAL: "normal",
        Priority.HIGH: "high",
        Priority.URGENT: "urgent",
    }

    with get_session(app_ctx.engine) as session:
        tasks = repo.list_by_status(session, done=False, limit=limit)
        if all:
            tasks += repo.list_by_status(session, done=True, limit=limit)

    if not tasks:
        console.print("[dim]Sin tareas pendientes.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Título")
    table.add_column("Prioridad", width=8)
    table.add_column("Vence", style="dim", width=12)
    table.add_column("Estado", width=8)

    for t in tasks:
        p = Priority(t.priority)
        table.add_row(
            str(t.id),
            t.title,
            f"[{pcolor[p]}]{plabel[p]}[/{pcolor[p]}]",
            str(t.due_date) if t.due_date else "—",
            "[green]done[/green]" if t.done else "[dim]pending[/dim]",
        )
    console.print(table)


@tasks_app.command("done")
def task_done(
    ctx: typer.Context,
    task_id: int = typer.Argument(..., help="ID de la tarea"),
) -> None:
    """Marca una tarea como completada."""
    from lumen.storage.db import get_session
    from lumen.storage.repositories import TaskRepository

    app_ctx = _get_ctx(ctx)
    repo = TaskRepository()
    with get_session(app_ctx.engine) as session:
        task = repo.mark_done(session, task_id)

    if task:
        console.print(f"[green]✓[/green] Tarea {task_id} completada.")
    else:
        console.print(f"[red]Tarea {task_id} no encontrada.[/red]")


@tasks_app.command("delete")
def task_delete(
    ctx: typer.Context,
    task_id: int = typer.Argument(..., help="ID de la tarea"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Elimina una tarea."""
    from lumen.storage.db import get_session
    from lumen.storage.repositories import TaskRepository

    if not yes:
        typer.confirm(f"¿Eliminar tarea {task_id}?", abort=True)

    app_ctx = _get_ctx(ctx)
    repo = TaskRepository()
    with get_session(app_ctx.engine) as session:
        ok = repo.delete(session, task_id)

    if ok:
        console.print(f"[green]✓[/green] Tarea {task_id} eliminada.")
    else:
        console.print(f"[red]Tarea {task_id} no encontrada.[/red]")
