"""Application factory and public foundation health checks."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from app.config import Settings
from app.database import get_engine
from app.schemas import ErrorResponse, HealthResponse, ReadinessResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    if get_engine.cache_info().currsize:
        get_engine().dispose()
        get_engine.cache_clear()


def error_response(status: int, code: str, message: str, details: object = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"code": code, "message": message, "details": jsonable_encoder(details)},
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="MapFlow AI API",
        description="Phase A — M1 foundation. Chỉ phục vụ kho mô phỏng.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(Settings.from_environment().cors_origins),
        allow_methods=["GET"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(HTTPException)
    async def handle_http_error(_request: Request, exc: HTTPException) -> JSONResponse:
        return error_response(exc.status_code, f"HTTP_{exc.status_code}", str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return error_response(
            422,
            "VALIDATION_ERROR",
            "Dữ liệu không hợp lệ.",
            {"errors": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_request: Request, _exc: Exception) -> JSONResponse:
        logger.exception("Unhandled API error")
        return error_response(500, "INTERNAL_ERROR", "Lỗi hệ thống.")

    @app.get(
        "/health",
        tags=["health"],
        summary="Liveness check",
        operation_id="get_health",
    )
    def get_health() -> HealthResponse:
        return HealthResponse(status="ok", service="mapflow-api", version="0.1.0", simulation=True)

    @app.get(
        "/health/ready",
        tags=["health"],
        summary="PostgreSQL readiness check",
        operation_id="get_readiness",
        responses={503: {"model": ErrorResponse, "description": "Database unavailable"}},
        response_model=ReadinessResponse,
    )
    def get_readiness() -> ReadinessResponse | JSONResponse:
        try:
            with get_engine().connect() as connection:
                connection.execute(text("SELECT 1"))
        except (SQLAlchemyError, RuntimeError):
            return error_response(503, "DATABASE_UNAVAILABLE", "Chưa kết nối được PostgreSQL.")
        return ReadinessResponse(status="ready", database="ok", simulation=True)

    return app


app = create_app()
