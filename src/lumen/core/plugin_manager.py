# src\lumen\core\plugin_manager.py
from __future__ import annotations

import importlib.metadata

import pluggy

from lumen.core.hookspecs import LumenSpec


class PluginManager:
    def __init__(self) -> None:
        self._pm = pluggy.PluginManager("lumen")
        self._pm.add_hookspecs(LumenSpec)

    def load_builtin_plugins(self) -> None:
        from lumen.builtin_plugins import notes, tasks

        self._pm.register(notes.NotesPlugin(), name="notes")
        self._pm.register(tasks.TasksPlugin(), name="tasks")

    def load_external_plugins(self) -> None:
        for ep in importlib.metadata.entry_points(group="lumen.plugins"):
            # Skip built-ins (already loaded directly above).
            if ep.name in ("notes", "tasks"):
                continue
            module = ep.load()
            plugin_cls = getattr(module, "Plugin", None)
            if plugin_cls:
                self._pm.register(plugin_cls(), name=ep.name)

    def load_all(self) -> None:
        self.load_builtin_plugins()
        self.load_external_plugins()

    @property
    def hook(self) -> pluggy.HookRelay:
        return self._pm.hook

    def list_plugins(self) -> list[str]:
        return [str(p) for p in self._pm.get_plugins()]
