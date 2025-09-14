"""MCP server exposing read-only Windchill tools over stdio."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from mcp.server import Server, tool

from src.config import BASE_URL
from src.windchill_client import WindchillClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("windchill.server")

server = Server(name="windchill-mcp", version="0.1.0")
client = WindchillClient()


@tool()
def health_check() -> Dict[str, str]:
    """Return service availability status."""
    try:
        return {"ok": "true", "base_url": BASE_URL}
    except Exception as exc:  # pragma: no cover - unexpected
        return {"ok": f"false: {exc}", "base_url": BASE_URL}


@tool()
def list_parts(container: str, limit: int = 20, state: str = "") -> List[Dict[str, Any]]:
    """List parts from a container."""
    if not container.strip():
        raise ValueError("container is required")
    if not isinstance(limit, int):  # type: ignore[unreachable]
        raise ValueError("limit must be int")
    limit = max(1, min(int(limit), 200))
    state = state.strip()
    logger.info(
        "list_parts", extra={"container": container, "limit": limit, "state": state}
    )
    parts = client.list_parts(container, limit, state)
    return [p.model_dump() for p in parts]


@tool()
def get_part(partNumber: str) -> Dict[str, Any]:
    """Retrieve a single part by part number."""
    if not partNumber.strip():
        raise ValueError("partNumber is required")
    logger.info("get_part", extra={"partNumber": partNumber})
    part = client.get_part(partNumber)
    return part.model_dump()


if __name__ == "__main__":
    print("Windchill MCP server ready (stdio).")
    server.run_stdio()
