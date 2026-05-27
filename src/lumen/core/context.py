from __future__ import annotations
from dataclasses import dataclass, field
from lumen.core.config import LumenConfig
from lumen.core.event_bus import EventBus
from lumen.storage.db import get_engine, init_db
from sqlalchemy import Engine


@dataclass
class AppContext:
    config: LumenConfig
    engine: Engine
    event_bus: EventBus = field(default_factory=EventBus)
    # plugin_manager se asigna después para evitar import circular
    plugin_manager: object = field(default=None)


def create_context() -> AppContext:
    config = LumenConfig()
    config.ensure_dirs()
    engine = get_engine(config.db_path)
    init_db(engine)
    return AppContext(config=config, engine=engine)
