from __future__ import annotations

import json
from typing import Any, Iterable, Mapping
from urllib.parse import parse_qs


def collapse_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    """Preserve repeated values while keeping scalar values convenient."""
    grouped: dict[str, list[Any]] = {}
    for key, value in pairs:
        grouped.setdefault(str(key), []).append(value)
    return {key: values[0] if len(values) == 1 else values for key, values in grouped.items()}


def collapse_lists(pairs: Iterable[tuple[str, list[Any]]]) -> dict[str, Any]:
    return {str(key): values[0] if len(values) == 1 else list(values) for key, values in pairs}


def parse_query(value: bytes | str) -> dict[str, Any]:
    if isinstance(value, bytes):
        value = value.decode("utf-8", "replace")
    parsed = parse_qs(value, keep_blank_values=True)
    return {key: values[0] if len(values) == 1 else values for key, values in parsed.items()}


def decode_body(body: bytes, content_type: str) -> tuple[Any, Mapping[str, Any]]:
    media_type = content_type.partition(";")[0].strip().lower()
    if not body:
        return None, {}
    if media_type == "application/json" or media_type.endswith("+json"):
        return json.loads(body)
    if media_type == "application/x-www-form-urlencoded":
        form = parse_query(body)
        return None, form
    return body, {}


def encode_body(value: Any, media_type: str) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if media_type == "application/json":
        try:
            import orjson

            return orjson.dumps(value)
        except ImportError:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return str(value).encode("utf-8")
