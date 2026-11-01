"""Contract-first: runtime OpenAPI must match the checked-in contract exactly."""

import json
from pathlib import Path

from app.main import create_app

ROOT = Path(__file__).resolve().parents[2]


def test_runtime_openapi_matches_contract() -> None:
    contract = json.loads((ROOT / "docs/openapi.json").read_text(encoding="utf-8"))
    assert create_app().openapi() == contract
