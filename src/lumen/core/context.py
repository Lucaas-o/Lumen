# src\lumen\core\context.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import Engine

from lumen.core.config import LumenConfig
from lumen.core.event_bus import EventBus
from lumen.storage.db import get_engine, init_db


@dataclass
class AppContext:
    config: LumenConfig
    engine: Engine
    event_bus: EventBus = field(default_factory=EventBus)
    # plugin_manager se asigna después para evitar import circular.
    # Tipado como Any para no acoplar AppContext a PluginManager.
    plugin_manager: Any = field(default=None)


def create_context() -> AppContext:
    config = LumenConfig()
    config.ensure_dirs()
    engine = get_engine(config.db_path)
    init_db(engine)
    return AppContext(config=config, engine=engine)
