from __future__ import annotations

import pytest

from src.windchill_client import WindchillClient


def test_get_part_not_found(monkeypatch) -> None:
    client = WindchillClient()

    def fake_get(self, path, params=None):  # type: ignore[override]
        raise RuntimeError("HTTP 404: not found")

    monkeypatch.setattr(WindchillClient, "get", fake_get)
    with pytest.raises(RuntimeError) as exc:
        client.get_part("MISSING")
    assert "404" in str(exc.value)
