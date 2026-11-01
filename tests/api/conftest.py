"""Small ASGI request harness using only pytest and Python's standard library."""

import asyncio
import json
from collections.abc import Callable
from typing import Any

import pytest
from fastapi import FastAPI

from app.database import get_engine
from app.main import create_app


def request(app: FastAPI, path: str, method: str = "GET") -> tuple[int, Any]:
    async def run() -> tuple[int, Any]:
        messages: list[dict[str, Any]] = []

        async def receive() -> dict[str, Any]:
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message: dict[str, Any]) -> None:
            messages.append(message)

        await app(
            {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
                "method": method,
                "scheme": "http",
                "path": path,
                "raw_path": path.encode(),
                "query_string": b"",
                "root_path": "",
                "headers": [],
                "client": ("127.0.0.1", 1234),
                "server": ("testserver", 80),
            },
            receive,
            send,
        )
        status = next(item["status"] for item in messages if item["type"] == "http.response.start")
        body = b"".join(
            item.get("body", b"") for item in messages if item["type"] == "http.response.body"
        )
        return status, json.loads(body)

    return asyncio.run(run())


@pytest.fixture
def api(monkeypatch: pytest.MonkeyPatch) -> Callable[..., tuple[int, Any]]:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    get_engine.cache_clear()
    app = create_app()

    def send_request(path: str, method: str = "GET") -> tuple[int, Any]:
        return request(app, path, method)

    return send_request
