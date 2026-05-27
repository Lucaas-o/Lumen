# src\lumen\core\event_bus.py
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event: str, callback: Callable[..., Any]) -> None:
        self._listeners[event].append(callback)

    def emit(self, event: str, **kwargs: Any) -> None:
        for callback in self._listeners.get(event, []):
            callback(**kwargs)


# Eventos built-in del sistema
class Events:
    NOTE_CREATED = "note.created"
    NOTE_DELETED = "note.deleted"
    TASK_CREATED = "task.created"
    TASK_DONE = "task.done"
    PLUGIN_LOADED = "plugin.loaded"
