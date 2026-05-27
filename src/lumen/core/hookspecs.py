# src\lumen\core\hookspecs.py
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pluggy

if TYPE_CHECKING:
    import typer

    from lumen.core.context import AppContext

hookspec = pluggy.HookspecMarker("lumen")


@dataclass
class SearchResult:
    title: str
    body: str
    source: str  # nombre del plugin que generó el resultado


class LumenSpec:
    @hookspec
    def register_commands(self, cli: typer.Typer) -> None:
        """El plugin registra sus subcomandos en el CLI principal."""
        ...

    @hookspec
    def on_startup(self, ctx: AppContext) -> None:
        """Se ejecuta una vez al arrancar Lumen."""
        ...

    @hookspec
    def on_shutdown(self, ctx: AppContext) -> None:
        """Se ejecuta al cerrar Lumen."""
        ...

    @hookspec
    def get_search_results(  # type: ignore[empty-body]
        self, query: str, ctx: AppContext
    ) -> list[SearchResult]:
        """Devuelve resultados de búsqueda para el query dado."""
        ...
