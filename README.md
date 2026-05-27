# Lumen

[![CI](https://github.com/TU_USUARIO/lumen/actions/workflows/ci.yml/badge.svg)](https://github.com/TU_USUARIO/lumen/actions)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Your extensible second brain in the terminal.

Lumen is a CLI/TUI tool for developers who live in their terminal. Notes, tasks, snippets, bookmarks — all in one place, extensible via plugins.

## Install

```bash
uv tool install lumen-cli
```

## Quick start

```bash
lumen note add "Idea para el proyecto"
lumen note ls
lumen task add "Terminar el README" --due tomorrow
lumen task ls
lumen search "proyecto"
```

## Extend

```bash
pip install lumen-plugin-pomodoro
lumen plugins ls
```

## Docs

Coming soon at [lumen.dev](https://lumen.dev)

## Status

Pre-alpha. Under active development.
