# Lumen — Plan de desarrollo

> Versión del plan: 0.1  
> Última actualización: 2026-05-27  
> Estado actual: Fase 0 — Setup

---

## Índice

1. [Filosofía del proyecto](#filosofía-del-proyecto)
2. [GitHub Projects — estructura](#github-projects--estructura)
3. [Fases de desarrollo](#fases-de-desarrollo)
4. [Orden de implementación de archivos](#orden-de-implementación-de-archivos)
5. [Requisitos por archivo](#requisitos-por-archivo)

---

## Filosofía del proyecto

Lumen es un segundo cerebro CLI/TUI extensible para developers.  
Reglas que guían cada decisión de diseño:

- **Funciona offline, siempre.** Sin servidores requeridos para operar.
- **Plugin-first.** Cada feature nueva es un plugin, no una modificación del core.
- **Instalación en un comando.** `uv tool install lumen-cli` y listo.
- **Usarlo tú primero.** Si no resuelve tu propio problema, reescribe o elimina.

---

## GitHub Projects — estructura

Usar un único Project con vistas distintas:

```
Proyecto: Lumen Development
├── Vista 1: Board (Kanban)
│   └── Columnas: Backlog | Ready | In Progress | Done
├── Vista 2: Roadmap (Timeline)
│   └── Agrupa por: Milestone
└── Vista 3: Table
    └── Filtro por: Label
```

### Milestones (crear en GitHub → Issues → Milestones)

| Milestone     | Descripción                          | Plazo estimado |
|---------------|--------------------------------------|----------------|
| `v0.1-setup`  | Repo, CI, pyproject funcional        | Semana 1-2     |
| `v0.2-core`   | Config, DB, hookspecs, plugin manager| Mes 1-2        |
| `v0.3-mvp`    | CLI notes + tasks funcionando        | Mes 2-3        |
| `v0.4-plugins`| Notas y tareas como plugins formales | Mes 4          |
| `v0.5-tui`    | TUI con Textual                      | Mes 5-7        |
| `v1.0-launch` | Docs pulidas, PyPI, lanzamiento      | Mes 12-14      |

### Labels a crear en GitHub

```
# Tipo
type: bug          #d73a4a
type: feature      #0e8a16
type: chore        #fef2c0
type: docs         #0075ca
type: refactor     #e4e669

# Área
area: core         #c5def5
area: cli          #bfd4f2
area: storage      #d4c5f9
area: plugins      #b2dfdb
area: tui          #ffe4b5
area: docs         #f9d0c4

# Dificultad (para cuando haya contributors)
good first issue   #7057ff
help wanted        #008672
```

### Plantilla de issue recomendada

Para el día a día, los issues son simplemente:
- Título claro: `[área] descripción breve`
- Milestone asignado
- Label de tipo + área

No hace falta más mientras seas el único desarrollador.

---

## Fases de desarrollo

### FASE 0 — Setup del repo (semanas 1-2)
**Objetivo:** que el repo esté en un estado limpio, instalable y con CI verde.

**Archivos a completar (en orden):**
1. `pyproject.toml`
2. `.gitignore`
3. `src/lumen/__init__.py`
4. `.github/workflows/ci.yml`
5. `README.md` (versión mínima)

**Criterio de salida:** `uv sync` funciona, `pytest` pasa (aunque no haya tests aún), ruff no reporta errores.

---

### FASE 1 — Core (mes 1-2)
**Objetivo:** el núcleo está en pie. Config cargada, DB conectada, plugin manager funcionando sin plugins reales todavía.

**Archivos a completar (en orden):**
1. `src/lumen/core/config.py`
2. `src/lumen/storage/db.py`
3. `src/lumen/core/context.py`
4. `src/lumen/core/hookspecs.py`
5. `src/lumen/core/plugin_manager.py`
6. `src/lumen/core/event_bus.py`
7. `src/lumen/cli/main.py`

**Criterio de salida:** `lumen --help` muestra la CLI. `lumen` arranca, carga config, conecta a SQLite, y lista plugins (vacío por ahora).

---

### FASE 2 — MVP (mes 2-3)
**Objetivo:** las dos funcionalidades más útiles funcionan end-to-end.

**Archivos a completar (en orden):**
1. `src/lumen/domain/note.py`
2. `src/lumen/domain/task.py`
3. `src/lumen/domain/tag.py`
4. `src/lumen/storage/repositories.py`
5. `src/lumen/builtin_plugins/notes/__init__.py`
6. `src/lumen/cli/notes.py`
7. `src/lumen/builtin_plugins/tasks/__init__.py`
8. `src/lumen/cli/tasks.py`

**Criterio de salida:** los comandos siguientes funcionan y persisten en SQLite:
```
lumen note add "mi primera nota"
lumen note ls
lumen task add "hacer algo" --due tomorrow
lumen task done 1
lumen search "primera"
```

---

### FASE 3 — Plugins formales (mes 4)
**Objetivo:** refactorizar para que notes y tasks sean plugins reales. Documentar cómo crear un plugin externo.

**Archivos a completar:**
1. `src/lumen/core/plugin_manager.py` (revisión)
2. `src/lumen/cli/plugins.py`
3. `examples/plugins/` (plugin de ejemplo mínimo)
4. `docs/plugins/index.md`

**Criterio de salida:** se puede instalar un plugin externo con `pip install lumen-plugin-X` y Lumen lo detecta automáticamente.

---

### FASE 4 — TUI (mes 5-7)
**Objetivo:** interfaz visual en terminal para navegar notas y tareas.

**Archivos a completar:**
1. `src/lumen/tui/app.py`
2. `src/lumen/tui/screens/` (pantallas según necesidad)

**Criterio de salida:** `lumen tui` abre una interfaz navegable con Textual.

---

### FASE 5 — Más plugins built-in (mes 8-12)
Uno por mes, según prioridad personal:
- `builtin_plugins/snippets/`
- `builtin_plugins/bookmarks/`
- (plugins adicionales según uso real)

---

### FASE 6 — v1.0 y lanzamiento (mes 12-14)
- Docs completas en MkDocs Material
- `CHANGELOG.md` actualizado
- Publicación en PyPI
- Post en HN / Reddit / dev.to

---

## Orden de implementación de archivos

Tabla de referencia rápida. Columna "Bloquea" indica qué no puedes hacer sin ese archivo.

| Orden | Archivo | Fase | Bloquea |
|-------|---------|------|---------|
| 1 | `pyproject.toml` | 0 | Todo lo demás |
| 2 | `.gitignore` | 0 | — |
| 3 | `src/lumen/__init__.py` | 0 | Imports del paquete |
| 4 | `.github/workflows/ci.yml` | 0 | CI automático |
| 5 | `core/config.py` | 1 | Context, CLI |
| 6 | `storage/db.py` | 1 | Repositories, dominio |
| 7 | `core/context.py` | 1 | Plugin manager, CLI |
| 8 | `core/hookspecs.py` | 1 | Plugin manager |
| 9 | `core/plugin_manager.py` | 1 | CLI main, plugins |
| 10 | `core/event_bus.py` | 1 | Plugins avanzados |
| 11 | `cli/main.py` | 1 | Punto de entrada |
| 12 | `domain/note.py` | 2 | Plugin notes |
| 13 | `domain/task.py` | 2 | Plugin tasks |
| 14 | `domain/tag.py` | 2 | Notes, tasks |
| 15 | `storage/repositories.py` | 2 | Plugins |
| 16 | `builtin_plugins/notes/__init__.py` | 2 | CLI notes |
| 17 | `cli/notes.py` | 2 | MVP |
| 18 | `builtin_plugins/tasks/__init__.py` | 2 | CLI tasks |
| 19 | `cli/tasks.py` | 2 | MVP |
| 20 | `cli/plugins.py` | 3 | Gestión plugins |
| 21 | `tui/app.py` | 4 | TUI |
| 22 | `builtin_plugins/snippets/` | 5 | — |
| 23 | `builtin_plugins/bookmarks/` | 5 | — |

---

## Requisitos por archivo

### `pyproject.toml`
- Nombre del paquete: `lumen-cli`
- Entry point CLI: `lumen = "lumen.cli.main:app"`
- Dependencias mínimas fase 0-1:
  - `typer >= 0.12`
  - `rich >= 13`
  - `pydantic >= 2.0`
  - `pydantic-settings >= 2.0`
  - `sqlmodel >= 0.0.19`
  - `pluggy >= 1.4`
- Dependencias dev:
  - `pytest`, `pytest-cov`, `ruff`, `mypy`
- Build backend: `hatchling`
- Python requerido: `>=3.12`

---

### `src/lumen/__init__.py`
- Solo exponer la versión: `__version__ = "0.1.0"`
- No importar nada más aquí (evita imports circulares)

---

### `core/config.py`
- Clase `LumenConfig` basada en `pydantic_settings.BaseSettings`
- Lee desde `~/.lumen/config.toml` y variables de entorno con prefijo `LUMEN_`
- Campos mínimos:
  - `data_dir: Path` → por defecto `~/.lumen/`
  - `db_path: Path` → por defecto `~/.lumen/lumen.db`
  - `plugins_enabled: list[str]` → lista de plugins activos
  - `log_level: str` → por defecto `"INFO"`
- Método `ensure_dirs()` que crea `data_dir` si no existe

---

### `storage/db.py`
- Función `get_engine(db_path: Path) -> Engine` usando SQLModel
- Función `init_db(engine)` que crea todas las tablas
- Usar SQLite con `check_same_thread=False`
- Preparado para migraciones futuras con Alembic (no implementar aún, solo dejar el comentario)

---

### `core/context.py`
- Clase `AppContext` con:
  - `config: LumenConfig`
  - `engine: Engine`
  - `plugin_manager: PluginManager`
  - `event_bus: EventBus`
- Función `create_context() -> AppContext` que inicializa todo en orden
- Este objeto se pasa a todos los plugins y comandos CLI

---

### `core/hookspecs.py`
- Clase `LumenSpec` con `@hookspec` para cada hook:
  - `register_commands(cli: typer.Typer)` — el plugin añade sus subcomandos
  - `on_startup(ctx: AppContext)` — se ejecuta al arrancar
  - `on_shutdown(ctx: AppContext)` — se ejecuta al cerrar
  - `get_search_results(query: str, ctx: AppContext) -> list[SearchResult]` — búsqueda global
- `SearchResult`: dataclass simple con `title`, `body`, `source` (nombre del plugin)

---

### `core/plugin_manager.py`
- Clase `PluginManager` que envuelve `pluggy.PluginManager`
- Método `load_builtin_plugins()` — carga los plugins de `builtin_plugins/`
- Método `load_external_plugins()` — descubre plugins via entry points (`lumen.plugins`)
- Método `get_hook()` — acceso a los hooks
- Al cargar un plugin, registrarlo en SQLite para tener historial (opcional fase 3)

---

### `core/event_bus.py`
- Implementación simple con un dict `{event_name: [callbacks]}`
- Métodos: `subscribe(event, callback)`, `emit(event, **kwargs)`
- Eventos base: `note.created`, `note.deleted`, `task.created`, `task.done`
- No usar dependencias externas, implementación pura Python

---

### `cli/main.py`
- Instancia de `typer.Typer()` llamada `app`
- Callback principal que inicializa `AppContext` y lo pasa via `typer.Context`
- Llama a `plugin_manager.load_all()` y luego a `register_commands` de cada plugin
- Comando `lumen version` que imprime la versión
- Comando `lumen plugins ls` que lista plugins cargados
- Usar `rich` para todo el output (nunca `print` plano)

---

### `domain/note.py`
- Clase `Note` como `SQLModel` con `table=True`
- Campos:
  - `id: int | None` (primary key, autoincrement)
  - `title: str`
  - `body: str`
  - `tags: str` (JSON serializado, simplificar para el MVP)
  - `created_at: datetime`
  - `updated_at: datetime`
  - `pinned: bool = False`
- Validaciones con pydantic: `title` no puede estar vacío

---

### `domain/task.py`
- Clase `Task` como `SQLModel` con `table=True`
- Campos:
  - `id: int | None`
  - `title: str`
  - `done: bool = False`
  - `due_date: date | None`
  - `priority: int = 0` (0=normal, 1=high, 2=urgent)
  - `tags: str` (JSON)
  - `created_at: datetime`
  - `done_at: datetime | None`

---

### `domain/tag.py`
- Clase `Tag` como `SQLModel`
- Campos: `id`, `name: str` (único), `color: str | None`
- Relación many-to-many con notes y tasks (tabla intermedia)
- En el MVP se puede simplificar con tags como JSON en cada entidad

---

### `storage/repositories.py`
- `NoteRepository`: CRUD para `Note`
  - `create(title, body, tags) -> Note`
  - `get(id) -> Note | None`
  - `list(limit, offset, tag_filter) -> list[Note]`
  - `search(query) -> list[Note]` (LIKE básico en MVP, FTS5 después)
  - `delete(id) -> bool`
  - `update(id, **fields) -> Note`
- `TaskRepository`: CRUD para `Task`
  - `create(title, due_date, priority) -> Task`
  - `get(id) -> Task | None`
  - `list(done, limit) -> list[Task]`
  - `mark_done(id) -> Task`
  - `delete(id) -> bool`
- Cada método recibe la `Session` como parámetro (no guardarla en el repo)

---

### `builtin_plugins/notes/__init__.py`
- Clase `NotesPlugin` con `@hookimpl`
- Implementa `register_commands(cli)`: añade el subcomando `lumen note`
- Implementa `get_search_results(query, ctx)`: busca en notas y devuelve `SearchResult`
- Implementa `on_startup(ctx)`: nada por ahora, reservado

---

### `cli/notes.py`
- Subapp `typer.Typer()` para el grupo `note`
- Comandos:
  - `note add <title> [--body TEXT] [--tag TAG]...`
  - `note ls [--tag TAG] [--limit N]`
  - `note show <id>`
  - `note edit <id>` (abre `$EDITOR`)
  - `note delete <id>`
  - `note search <query>`
- Output con `rich.table.Table` para `ls`, `rich.panel.Panel` para `show`

---

### `builtin_plugins/tasks/__init__.py`
- Igual que `notes` pero para tareas
- Implementa `get_search_results` buscando en tareas pendientes

---

### `cli/tasks.py`
- Comandos:
  - `task add <title> [--due DATE] [--priority high|normal|urgent]`
  - `task ls [--all] [--due today|week]`
  - `task done <id>`
  - `task delete <id>`
  - `task show <id>`
- Output con `rich` (tabla para `ls`, colores por prioridad)

---

### `.github/workflows/ci.yml`
- Trigger: push a `main`, pull requests
- Jobs:
  - `lint`: ruff check + ruff format --check
  - `typecheck`: mypy src/
  - `test`: pytest con coverage en Python 3.12 y 3.13
  - Matriz: ubuntu-latest + windows-latest
- Cache de dependencias con uv

---

### `README.md` (versión inicial)
- Badge de CI
- Una línea de qué es Lumen
- Instalación: `uv tool install lumen-cli`
- 5 comandos de ejemplo
- Link a docs
- No escribir más hasta tener algo funcionando

---

## Notas de mantenimiento del plan

- Actualizar este archivo cada vez que completes una fase
- Marcar archivos completados con ~~tachado~~ en las tablas
- Si cambias una decisión de arquitectura, añadir una entrada en `CHANGELOG.md`
- No añadir nuevas features al backlog sin haberlas pensado al menos 24h

