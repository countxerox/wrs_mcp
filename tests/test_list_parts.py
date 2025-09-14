from __future__ import annotations

from src.windchill_client import WindchillClient


def test_list_parts(monkeypatch) -> None:
    client = WindchillClient()

    def fake_get(self, path, params=None):  # type: ignore[override]
        assert path == "containers/demo/parts"
        assert params == {
            "$top": 2,
            "$orderby": "createdOn desc",
            "$filter": "lifecycleState eq 'RELEASED'",
        }
        return {
            "items": [
                {
                    "number": "123",
                    "name": "Bolt",
                    "iteration": "A",
                    "lifecycleState": "RELEASED",
                    "createdOn": "2024-01-01",
                },
                {
                    "number": "124",
                    "name": "Nut",
                    "iteration": "B",
                    "lifecycleState": "RELEASED",
                    "createdOn": "2024-01-02",
                },
            ]
        }

    monkeypatch.setattr(WindchillClient, "get", fake_get)
    parts = client.list_parts("demo", limit=2, state="RELEASED")
    assert len(parts) == 2
    assert parts[0].partNumber == "123"
    assert parts[1].name == "Nut"
