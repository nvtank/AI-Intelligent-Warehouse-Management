"""Generate the subset of OpenAPI TypeScript types used by this milestone.

Uses only the Python standard library. Unsupported schemas fail explicitly.
"""

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/openapi.json"
OUTPUT = ROOT / "apps/web/src/api/generated.ts"


def schema_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        prefix = "#/components/schemas/"
        if not schema["$ref"].startswith(prefix):
            raise ValueError(f"Unsupported reference: {schema['$ref']}")
        return f"Schemas[{json.dumps(schema['$ref'][len(prefix) :])}]"
    if "const" in schema:
        return json.dumps(schema["const"], ensure_ascii=False)
    if "enum" in schema:
        return " | ".join(json.dumps(value, ensure_ascii=False) for value in schema["enum"])
    if "anyOf" in schema:
        return " | ".join(schema_type(item) for item in schema["anyOf"])
    kind = schema.get("type")
    if kind == "object":
        required = schema.get("required", [])
        fields = [
            f"{json.dumps(name)}{'' if name in required else '?'}: {schema_type(value)};"
            for name, value in schema.get("properties", {}).items()
        ]
        additional = schema.get("additionalProperties")
        if additional is True:
            fields.append("[key: string]: unknown;")
        elif isinstance(additional, dict):
            fields.append(f"[key: string]: {schema_type(additional)};")
        return "{ " + " ".join(fields) + " }"
    if kind == "array":
        return f"Array<{schema_type(schema['items'])}>"
    primitive = {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "null": "null",
    }
    if kind in primitive:
        return primitive[kind]
    if schema == {}:
        return "unknown"
    raise ValueError(f"Unsupported OpenAPI schema: {schema}")


def generate(contract: dict[str, Any]) -> str:
    lines = [
        "// Generated from docs/openapi.json. Do not edit by hand.",
        "// Run: npm run types:generate",
        "export interface Schemas {",
    ]
    for name, schema in contract["components"]["schemas"].items():
        lines.append(f"  {json.dumps(name)}: {schema_type(schema)};")
    lines.extend(["}", "", "export interface Operations {"])
    for path_item in contract["paths"].values():
        for method, operation in path_item.items():
            if method not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                raise ValueError(f"Unsupported path entry: {method}")
            lines.append(f"  {json.dumps(operation['operationId'])}: {{ responses: {{")
            for status, response in operation["responses"].items():
                if not status.isdecimal():
                    raise ValueError(f"Unsupported response status: {status}")
                schema = response["content"]["application/json"]["schema"]
                lines.append(f"    {status}: {schema_type(schema)};")
            lines.append("  } };")
    lines.extend(["}", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = generate(json.loads(CONTRACT.read_text(encoding="utf-8")))
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != generated:
            raise SystemExit("Generated web types are stale. Run npm run types:generate.")
        print("OpenAPI web types are up to date.")
    else:
        OUTPUT.write_text(generated, encoding="utf-8")
        print(f"Generated {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
