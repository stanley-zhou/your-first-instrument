# ADR-0006: `days_until` — the first tool, and three choices inside it

- Status: Accepted · 2026-10-09 · Stanley Zhou

**Decision**: Replace the `my_tool` stub with `days_until(event)`, which
returns the number of days to a personal milestone the model cannot know on
its own (Track A in docs/TRACKS.md).

**Choice 1: data lives in a dict in `server.py`.**
Options: JSON file · SQLite · environment variables · in-code dict.
Chosen: in-code dict. With two or three entries, "edit, commit, push" is the
shortest loop, and Render redeploys automatically. Cost: data and code are
mixed. Past roughly ten entries, the data should move out. Expected to be
superseded when the server gains persistent memory.

**Choice 2: an unknown event returns the list of known events, not an error.**
Options: raise `ValueError` · return a message that lists the known keys.
Chosen: return the list. The model sees only the tool's returned text. A
list lets it correct the call on the next turn without guessing. An
exception tells it only that something failed. Principle: a tool should
describe itself in its failure path, not only in its docstring.

**Choice 3: Track A before B or C.**
Options: A (personal instrument) · B (dataset liberator) · C (form).
Chosen: A, because it closes the full loop (edit, restart, verify, deploy)
in one session with a fact that is genuinely mine. B and C are natural next
tools, not replacements.

**If wrong**: If Claude keeps calling `days_until` with near-miss names
("grad", "commencement"), add fuzzy matching or aliases, and write a new ADR.
