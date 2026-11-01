"""Response models implementing docs/openapi.json."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["mapflow-api"]
    version: Literal["0.1.0"]
    simulation: Literal[True]


class ReadinessResponse(BaseModel):
    status: Literal["ready"]
    database: Literal["ok"]
    simulation: Literal[True]


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, object] | None
