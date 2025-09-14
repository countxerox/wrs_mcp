"""Minimal Windchill REST client with read-only operations."""

from __future__ import annotations

from typing import Any, Dict, List
import logging

import requests

from .config import API_TOKEN, BASE_URL, HTTP_TIMEOUT, VERIFY_TLS
from .models import Part

logger = logging.getLogger(__name__)


class WindchillClient:
    """HTTP client for querying Windchill REST/OData endpoints."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.base_url = BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
        }
        # Rate limit hint: consider adding client-side throttling here.

    def get(self, path: str, params: dict | None = None) -> Dict[str, Any]:
        """Perform a GET request and return parsed JSON."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.debug("GET %s", url)
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                params=params,
                timeout=HTTP_TIMEOUT,
                verify=VERIFY_TLS,
            )
            response.raise_for_status()
        except requests.HTTPError as exc:  # pragma: no cover - network error path
            snippet = response.text[:200]
            raise RuntimeError(f"HTTP {response.status_code}: {snippet}") from exc
        return response.json()

    def list_parts(self, container: str, limit: int, state: str) -> List[Part]:
        """List parts in a container.

        Placeholder endpoint; swap with real Windchill path.
        GET containers/{container}/parts?$top={limit}&$orderby=createdOn desc
        + optional $filter=lifecycleState eq '{state}'
        """
        params = {"$top": limit, "$orderby": "createdOn desc"}
        if state:
            params["$filter"] = f"lifecycleState eq '{state}'"
        path = f"containers/{container}/parts"
        data = self.get(path, params=params)
        items = data.get("items") or data.get("value") or []
        parts: List[Part] = []
        for raw in items:
            normalized = {
                "partNumber": raw.get("partNumber") or raw.get("number"),
                "name": raw.get("name"),
                "version": raw.get("version") or raw.get("iteration"),
                "state": raw.get("state") or raw.get("lifecycleState"),
                "createdOn": raw.get("createdOn"),
                "modifiedOn": raw.get("modifiedOn"),
            }
            parts.append(Part(**normalized))
        return parts

    def get_part(self, part_number: str) -> Part:
        """Fetch a single part by number.

        Placeholder endpoint; swap with real Windchill path.
        GET parts/{partNumber}
        """
        path = f"parts/{part_number}"
        data = self.get(path, params=None)
        normalized = {
            "partNumber": data.get("partNumber") or data.get("number"),
            "name": data.get("name"),
            "version": data.get("version") or data.get("iteration"),
            "state": data.get("state") or data.get("lifecycleState"),
            "createdOn": data.get("createdOn"),
            "modifiedOn": data.get("modifiedOn"),
        }
        return Part(**normalized)
