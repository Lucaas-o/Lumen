# src\lumen\core\config.py
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LumenConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="LUMEN_",
        toml_file="~/.lumen/config.toml",
    )

    data_dir: Path = Field(default=Path("~/.lumen").expanduser())
    db_path: Path = Field(default=Path("~/.lumen/lumen.db").expanduser())
    plugins_enabled: list[str] = Field(default=["notes", "tasks"])
    log_level: str = "INFO"

    def ensure_dirs(self) -> None:
        self.data_dir.expanduser().mkdir(parents=True, exist_ok=True)
