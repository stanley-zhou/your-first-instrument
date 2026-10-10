# ADR-0005: One source of truth for dependencies — Render installs from uv.lock

- Status: Accepted · 2026-10-09 · Stanley Zhou
- Supersedes: the interim "pin in both files" fix from 2026-09-17

**Context**: mcp 2.x renamed `FastMCP`, which broke 1.x code. `pyproject.toml`
pinned `mcp[cli]>=1.2,<2`, so local `uv run` worked. But the `buildCommand` in
`render.yaml` ran its own `pip install "mcp[cli]"` and never read
`pyproject.toml`. Render installed 2.x and the service crashed at startup.
The root cause was two independent install paths, with the constraint
written in only one of them.

**Options considered**:
- (A) Pin in `pyproject.toml` only. Proven insufficient, because Render
  bypasses it.
- (B) Pin in both files (the interim fix). It works, but every future change
  must be made twice. One missed edit brings the same failure back.
- (C) Make Render use uv and install from `uv.lock`. One file defines the
  dependencies, and both install paths read it. **Chosen.**
- (D) A Dockerfile. It also locks the Python version and system libraries,
  but it is too heavy for a server of this size.

**Decision**: `buildCommand: pip install uv && uv sync --frozen` and
`startCommand: uv run --frozen server.py`. `pyproject.toml` declares the
allowed ranges. `uv.lock` records the exact versions. Local and cloud
environments are built from the same lock.

**Consequences**: `--frozen` makes the build fail loudly if `uv.lock` is
stale, instead of silently resolving new versions. To change a dependency,
run `uv add` / `uv lock` locally, commit `uv.lock`, and push.

**Rule generalized**: a safeguard is only complete when it covers every path
the failure can take. The best way to cover every path is to have only one.

**If wrong**: If the build becomes too slow or uv is unavailable on the
host, fall back to (B), or move to (D) if the deployment grows.
