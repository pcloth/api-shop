"""Explicit, optional ORM-to-DTO inspectors.

ORM packages are imported lazily. Callers must select fields; this module never
serializes an entire model or follows relationships implicitly.
"""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, create_model


SENSITIVE_FIELDS = frozenset({"password", "password_hash", "secret", "token", "api_key"})


class ModelInspector(Protocol):
    def create_dto(self, model: type[Any], fields: list[str], *, name: str | None = None) -> type[BaseModel]: ...


def _check_fields(fields: list[str]) -> None:
    if not fields:
        raise ValueError("ORM DTO generation requires an explicit, non-empty field list")
    forbidden = SENSITIVE_FIELDS.intersection(field.lower() for field in fields)
    if forbidden:
        raise ValueError(f"Sensitive fields require a handwritten DTO: {sorted(forbidden)}")


class DjangoModelInspector:
    def create_dto(
        self, model: type[Any], fields: list[str], *, name: str | None = None
    ) -> type[BaseModel]:
        _check_fields(fields)
        selected: dict[str, tuple[Any, Any]] = {}
        for field_name in fields:
            try:
                model_field = model._meta.get_field(field_name)
            except Exception as exc:
                raise ValueError(f"Unknown Django model field {field_name!r}") from exc
            if getattr(model_field, "is_relation", False):
                raise ValueError(f"Relationship field {field_name!r} requires a handwritten DTO")
            python_type = _django_python_type(model_field)
            nullable = bool(getattr(model_field, "null", False))
            annotation = python_type | None if nullable else python_type
            default = None if nullable else ...
            selected[field_name] = (annotation, default)
        return create_model(
            name or f"{model.__name__}DTO",
            __config__=ConfigDict(from_attributes=True),
            **selected,
        )


class SQLAlchemyModelInspector:
    def create_dto(
        self, model: type[Any], fields: list[str], *, name: str | None = None
    ) -> type[BaseModel]:
        _check_fields(fields)
        try:
            columns = {column.name: column for column in model.__table__.columns}
        except AttributeError as exc:
            raise TypeError("Expected a SQLAlchemy declarative model") from exc
        selected: dict[str, tuple[Any, Any]] = {}
        for field_name in fields:
            if field_name not in columns:
                raise ValueError(f"Unknown SQLAlchemy column {field_name!r}")
            column = columns[field_name]
            try:
                python_type = column.type.python_type
            except (AttributeError, NotImplementedError):
                python_type = Any
            nullable = bool(column.nullable)
            annotation = python_type | None if nullable and python_type is not Any else python_type
            default = None if nullable else ...
            selected[field_name] = (annotation, default)
        return create_model(
            name or f"{model.__name__}DTO",
            __config__=ConfigDict(from_attributes=True),
            **selected,
        )


def _django_python_type(field: Any) -> type[Any]:
    mapping = {
        "AutoField": int,
        "BigAutoField": int,
        "IntegerField": int,
        "BigIntegerField": int,
        "SmallIntegerField": int,
        "PositiveIntegerField": int,
        "PositiveSmallIntegerField": int,
        "FloatField": float,
        "DecimalField": __import__("decimal").Decimal,
        "BooleanField": bool,
        "DateField": __import__("datetime").date,
        "DateTimeField": __import__("datetime").datetime,
        "TimeField": __import__("datetime").time,
        "UUIDField": __import__("uuid").UUID,
        "BinaryField": bytes,
        "JSONField": Any,
    }
    return mapping.get(field.get_internal_type(), str)

