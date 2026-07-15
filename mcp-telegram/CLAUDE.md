# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install package + dev dependencies (ruff, pyright, twine) with uv
uv pip install -e ".[dev]"

# Install pre-commit hooks (ruff-format, ruff --fix, uv.lock check, prettier)
pre-commit install

# Lint / format
ruff check .
ruff format .

# Type check (strict mode, applies only to src/mcp_telegram)
pyright

# Run the CLI locally during development
uv run mcp-telegram --help
uv run mcp-telegram login          # interactive Telegram auth, writes session file
uv run mcp-telegram start          # runs the MCP server (stdio) via mcp.run()
uv run mcp-telegram tools          # lists all registered MCP tools in a table
```

There is no test suite in this repo; verification is via `ruff`, `pyright`, and manual exercise of the CLI/MCP tools.

## Architecture

This package exposes a Telegram account (via MTProto/Telethon) as an MCP server, plus a Typer CLI for auth and diagnostics.

- **`cli.py`** — Typer app (`mcp-telegram` entry point, see `[project.scripts]` in `pyproject.toml`). Commands: `login` (interactive API ID/hash/phone/2FA flow, writes the Telethon session file), `start` (runs `mcp.run()` from `server.py`), `logout`/`clear-session` (session file management), `tools` (renders the MCP server's registered tools via `mcp.list_tools()`), `version`. Async commands are wrapped with the local `async_command` decorator to bridge Typer (sync) and asyncio.
- **`server.py`** — Defines the `FastMCP` instance (`mcp`) and every `@mcp.tool()`. Each tool is a thin wrapper: parse the `entity` argument with `parse_entity`, delegate the real work to the module-level `Telegram()` instance (`tg`), and return a pydantic model or plain string. `app_lifespan` connects the Telethon client on server startup and disconnects on shutdown — this is where `tg.create_client()` is first called, so `API_ID`/`API_HASH` env vars must be set before `start` runs.
- **`telegram.py`** — `Telegram` class wraps `telethon.TelegramClient` and holds all the actual Telegram/MTProto logic (send/edit/delete messages, drafts, message history with date-range + unread filtering, media download, dialog search, permission checks for whether the account can post into a given entity). Session and downloaded-media files live under `xdg_state_home()/mcp-telegram/` (via `xdg-base-dirs`), not in the repo. `Settings` (pydantic-settings `BaseSettings`) reads `API_ID`/`API_HASH` from the environment when `create_client` isn't given explicit credentials.
- **`types.py`** — Pydantic response models (`Dialog`, `Message`, `Media`, `DownloadedMedia`, `Messages`) returned by MCP tools. Each has a `from_entity`/`from_message` static constructor that converts the corresponding raw Telethon object (`telethon.hints.Entity`, `telethon.tl.patched.Message`, etc.) into the pydantic model — this is the boundary between Telethon's types and the MCP-facing schema.
- **`utils.py`** — Free functions used by both `server.py` and `telegram.py`: `parse_entity` (string → int ID or username/phone passthrough), `get_unique_filename` (collision-safe filenames for downloaded media), `parse_telegram_url` (regex-based parser for `t.me/...` message links, used by `message_from_link`).

**Data flow for a tool call:** MCP client → tool function in `server.py` → `parse_entity()` normalizes the identifier → `Telegram` method in `telegram.py` calls Telethon → raw Telethon object converted to a pydantic model from `types.py` → returned to the MCP client.

**Key constraint:** Telethon's SQLite-backed session file only supports one active connection at a time; running multiple `mcp-telegram` instances against the same session causes "database is locked" errors (see README troubleshooting section).
