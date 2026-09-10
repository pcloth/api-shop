"""Optional host-framework adapters for the framework-neutral dispatcher."""

from .asgi import ASGIAdapter
from .bottle import mount_bottle
from .django import django_urlpatterns
from .flask import mount_flask

__all__ = ["ASGIAdapter", "django_urlpatterns", "mount_flask", "mount_bottle"]
