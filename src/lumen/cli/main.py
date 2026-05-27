from __future__ import annotations

import typer
from rich import print as rprint
from rich.console import Console

from lumen import __version__

app = typer.Typer(
    name="lumen",
    help="Your extensible second brain in the terminal.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(ctx: typer.Context) -> None:
    from lumen.core.context import create_context
    from lumen.core.plugin_manager import PluginManager

    app_ctx = create_context()
    pm = PluginManager()
    pm.load_all()
    app_ctx.plugin_manager = pm

    pm.hook.register_commands(cli=app)
    pm.hook.on_startup(ctx=app_ctx)

    ctx.ensure_object(dict)
    ctx.obj = app_ctx


@app.command()
def version() -> None:
    """Muestra la versión de Lumen."""
    rprint(f"[bold]lumen[/bold] v{__version__}")


@app.command(name="search")
def search_cmd(
    query: str = typer.Argument(..., help="Texto a buscar"),
    ctx: typer.Context = typer.Option(None),
) -> None:
    """Busca en todas las fuentes (notas, tareas, etc.)."""
    app_ctx = ctx.obj
    results = app_ctx.plugin_manager.hook.get_search_results(
        query=query, ctx=app_ctx
    )
    flat = [r for sublist in results for r in sublist]
    if not flat:
        rprint("[dim]Sin resultados.[/dim]")
        return
    for r in flat:
        console.print(f"[bold]{r.title}[/bold] [dim]({r.source})[/dim]")
        if r.body:
            console.print(f"  {r.body[:80]}")


if __name__ == "__main__":
    app()