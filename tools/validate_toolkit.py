"""Validate toolkit.json: required fields, unique ids, HTTPS-only links and no bundled binaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = ("id", "name", "category", "purpose", "homepage", "download", "license", "platforms", "verification", "safe_use")
CATEGORIES = frozenset({"deploy", "edit", "mirror", "design"})
PLATFORMS = frozenset({"windows", "macos", "linux"})
BINARY_SUFFIXES = frozenset({".exe", ".msi", ".dmg", ".zip", ".7z", ".rar", ".bmp", ".iso"})


def validate(doc: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict) or doc.get("schema_version") != 1:
        return ["schema_version must be 1"]
    tools = doc.get("tools")
    if not isinstance(tools, list) or not tools:
        return ["tools must be a non-empty list"]
    seen: set[str] = set()
    for index, tool in enumerate(tools):
        where = f"tools[{index}]"
        if not isinstance(tool, dict):
            errors.append(f"{where}: must be an object")
            continue
        for key in REQUIRED:
            value = tool.get(key)
            if key == "platforms":
                if not isinstance(value, list) or not value or not set(value) <= PLATFORMS:
                    errors.append(f"{where}.platforms: must be a non-empty subset of {sorted(PLATFORMS)}")
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"{where}.{key}: required non-empty string")
        tool_id = tool.get("id")
        if isinstance(tool_id, str):
            if tool_id in seen:
                errors.append(f"{where}.id: duplicate '{tool_id}'")
            seen.add(tool_id)
        if tool.get("category") not in CATEGORIES:
            errors.append(f"{where}.category: must be one of {sorted(CATEGORIES)}")
        for key in ("homepage", "download"):
            link = tool.get(key)
            if isinstance(link, str):
                parsed = urlparse(link)
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(f"{where}.{key}: must be an absolute https URL")
                if Path(parsed.path).suffix.lower() in BINARY_SUFFIXES:
                    errors.append(f"{where}.{key}: must link to the publisher page, not a binary")
    return errors


def bundled_binaries(root: Path) -> list[str]:
    return sorted(
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts and p.suffix.lower() in BINARY_SUFFIXES
    )


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors = validate(json.loads((root / "toolkit.json").read_text(encoding="utf-8")))
    errors += [f"bundled binary not allowed: {name}" for name in bundled_binaries(root)]
    for error in errors:
        print(error, file=sys.stderr)
    print(f"toolkit: {'FAIL' if errors else 'OK'} ({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
