"""your-first-instrument — a sense of time for a model that has none.

Why time? Ask your Claude "how long have we been talking?" WITHOUT this
connected. It can only guess: no clock lives in a context window. This
server is the smallest honest fix — and the pattern generalizes to any
instrument you can imagine. See docs/adr/ for every choice made here.
"""
import os
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "your-first-instrument",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)

@mcp.tool()
def current_time() -> str:
    """The current date and time (UTC and local)."""
    now = datetime.now(timezone.utc)
    return f"UTC: {now.isoformat()} · local: {datetime.now().isoformat()}"

@mcp.tool()
def seconds_since(iso_timestamp: str) -> str:
    """Seconds elapsed since an ISO timestamp (e.g. '2026-09-10T17:15:00').
    Naive timestamps (no timezone) are read as LOCAL time."""
    then = datetime.fromisoformat(iso_timestamp)
    if then.tzinfo is None:
        then = then.replace(tzinfo=datetime.now().astimezone().tzinfo)
    delta = datetime.now(timezone.utc) - then
    return f"{delta.total_seconds():.0f} seconds ({delta})"

# Dates only I would know. Claude cannot guess these; it has to ask.
MY_DATES = {
    "graduation": "2027-05-17",
    "cis7000 next session": "2026-10-15",
    # add more: "name": "YYYY-MM-DD"
}

@mcp.tool()
def days_until(event: str) -> str:
    """Days until one of my personal milestones. Call with no argument or
    an unknown name to get the list of known events."""
    from datetime import date
    key = event.strip().lower()
    if key not in MY_DATES:
        known = ", ".join(MY_DATES)
        return f"Unknown event '{event}'. Known events: {known}"
    target = date.fromisoformat(MY_DATES[key])
    delta = (target - date.today()).days
    if delta > 0:
        return f"{delta} days until {event} ({target.isoformat()})"
    if delta == 0:
        return f"{event} is today ({target.isoformat()})"
    return f"{event} was {-delta} days ago ({target.isoformat()})"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
