"""Environment configuration without additional settings dependencies."""

import os
from dataclasses import dataclass

from sqlalchemy.engine import URL


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str
    cors_origins: tuple[str, ...]

    @classmethod
    def from_environment(cls) -> "Settings":
        database_url = os.environ.get("DATABASE_URL", "")
        # Components let Compose safely handle passwords containing URL characters.
        if not database_url and os.environ.get("POSTGRES_HOST"):
            database_url = URL.create(
                "postgresql+psycopg",
                username=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host=os.environ["POSTGRES_HOST"],
                port=int(os.environ.get("POSTGRES_PORT", "5432")),
                database=os.environ["POSTGRES_DB"],
            ).render_as_string(hide_password=False)
        return cls(
            database_url=database_url,
            cors_origins=tuple(
                origin.strip()
                for origin in os.environ.get("CORS_ORIGINS", "").split(",")
                if origin.strip()
            ),
        )
