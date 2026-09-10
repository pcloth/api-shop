from __future__ import annotations

import unittest

from api_shop.orm import DjangoModelInspector, SQLAlchemyModelInspector


class SQLAlchemyInspectorTests(unittest.TestCase):
    def test_explicit_fields_and_attribute_serialization(self):
        from sqlalchemy import Integer, String
        from sqlalchemy.orm import DeclarativeBase, mapped_column

        class Base(DeclarativeBase):
            pass

        class User(Base):
            __tablename__ = "users_v2_test"
            id = mapped_column(Integer, primary_key=True)
            name = mapped_column(String(50), nullable=False)
            password = mapped_column(String(50), nullable=False)

        inspector = SQLAlchemyModelInspector()
        dto = inspector.create_dto(User, ["id", "name"])
        self.assertEqual(dto.model_validate(User(id=1, name="Ada", password="hidden")).model_dump(), {"id": 1, "name": "Ada"})
        with self.assertRaisesRegex(ValueError, "Sensitive"):
            inspector.create_dto(User, ["password"])

    def test_field_list_is_required(self):
        with self.assertRaisesRegex(ValueError, "explicit"):
            SQLAlchemyModelInspector().create_dto(object, [])


class DjangoInspectorTests(unittest.TestCase):
    def test_explicit_fields_and_relationship_protection(self):
        from django.conf import settings

        if not settings.configured:
            settings.configure(INSTALLED_APPS=[], DEFAULT_CHARSET="utf-8")
        import django

        django.setup()
        from django.db import models

        class Team(models.Model):
            name = models.CharField(max_length=50)

            class Meta:
                app_label = "api_shop_tests"

        class Member(models.Model):
            name = models.CharField(max_length=50)
            password = models.CharField(max_length=50)
            team = models.ForeignKey(Team, on_delete=models.CASCADE)

            class Meta:
                app_label = "api_shop_tests"

        inspector = DjangoModelInspector()
        dto = inspector.create_dto(Member, ["id", "name"])
        self.assertEqual(
            dto.model_validate(Member(id=1, name="Ada", password="hidden")).model_dump(),
            {"id": 1, "name": "Ada"},
        )
        with self.assertRaisesRegex(ValueError, "Sensitive"):
            inspector.create_dto(Member, ["password"])
        with self.assertRaisesRegex(ValueError, "Relationship"):
            inspector.create_dto(Member, ["team"])
