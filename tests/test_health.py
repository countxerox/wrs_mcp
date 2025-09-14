from __future__ import annotations

from server import health_check
from src.config import BASE_URL


def test_health_check() -> None:
    result = health_check()
    assert result == {"ok": "true", "base_url": BASE_URL}
