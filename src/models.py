"""Pydantic models used by the Windchill MCP connector."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Part(BaseModel):
    partNumber: str
    name: str
    version: str
    state: str
    createdOn: Optional[str] = None
    modifiedOn: Optional[str] = None


class PartListResponse(BaseModel):
    items: list[Part]
