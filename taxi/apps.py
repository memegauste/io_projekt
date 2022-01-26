"""Taxi app config."""
from django.apps import AppConfig


class TaxiConfig(AppConfig):  # noqa: D101
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taxi'
