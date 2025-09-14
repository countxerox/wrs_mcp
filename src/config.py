"""Configuration values loaded from environment variables."""

from __future__ import annotations

import os


def _get_bool(name: str, default: str) -> bool:
    return os.getenv(name, default).lower() in {"1", "true", "yes"}


BASE_URL: str = os.getenv("WINDCHILL_BASE_URL", "")
API_TOKEN: str = os.getenv("WINDCHILL_API_TOKEN", "")
VERIFY_TLS: bool = _get_bool("VERIFY_TLS", "true")
HTTP_TIMEOUT: int = int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))

__all__ = ["BASE_URL", "API_TOKEN", "VERIFY_TLS", "HTTP_TIMEOUT"]
