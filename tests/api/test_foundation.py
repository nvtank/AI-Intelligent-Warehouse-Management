"""Foundation behavior and live PostgreSQL smoke test."""

from collections.abc import Callable
from typing import Any

import pytest
from conftest import request
from sqlalchemy import inspect

from app.config import Settings
from app.database import Base, get_engine
from app.main import create_app


def test_liveness_without_database(api: Callable[..., tuple[int, Any]]) -> None:
    status, body = api("/health")
    assert status == 200
    assert body == {
        "status": "ok",
        "service": "mapflow-api",
        "version": "0.1.0",
        "simulation": True,
    }


def test_readiness_without_configuration(api: Callable[..., tuple[int, Any]]) -> None:
    status, body = api("/health/ready")
    assert status == 503
    assert body == {
        "code": "DATABASE_UNAVAILABLE",
        "message": "Chưa kết nối được PostgreSQL.",
        "details": None,
    }


@pytest.mark.parametrize(
    ("path", "method", "expected"), [("/missing", "GET", 404), ("/health", "POST", 405)]
)
def test_error_envelope(
    api: Callable[..., tuple[int, Any]], path: str, method: str, expected: int
) -> None:
    status, body = api(path, method)
    assert status == expected
    assert set(body) == {"code", "message", "details"}
    assert body["code"] == f"HTTP_{expected}"


def test_readiness_when_database_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+psycopg://unavailable:unavailable@127.0.0.1:1/unavailable"
    )
    get_engine.cache_clear()
    try:
        status, body = request(create_app(), "/health/ready")
        assert status == 503
        assert body["code"] == "DATABASE_UNAVAILABLE"
        assert body["details"] is None
        assert "unavailable:" not in str(body)
    finally:
        get_engine().dispose()
        get_engine.cache_clear()


def test_no_business_tables_in_m1() -> None:
    assert not Base.metadata.tables


@pytest.mark.integration
def test_postgresql_readiness_and_empty_schema() -> None:
    if not Settings.from_environment().database_url:
        pytest.skip("Integration test requires DATABASE_URL pointing to PostgreSQL")
    get_engine.cache_clear()
    try:
        status, body = request(create_app(), "/health/ready")
        assert status == 200
        assert body == {"status": "ready", "database": "ok", "simulation": True}
        # M1 may contain Alembic's own metadata table, never a business table.
        assert set(inspect(get_engine()).get_table_names()) <= {"alembic_version"}
    finally:
        get_engine().dispose()
        get_engine.cache_clear()
