from sqlalchemy import create_engine, inspect

import missioncloud_value_hub.db.models  # noqa: F401
from missioncloud_value_hub.config import get_settings
from missioncloud_value_hub.db.base import Base

EXPECTED_TABLES = {
    "app_users",
    "audit_events",
    "business_units",
    "cloud_accounts",
    "cloud_services",
    "organizations",
    "roles",
    "teams",
    "user_roles",
}


def test_database_url_uses_psycopg_driver() -> None:
    settings = get_settings()

    assert settings.database_url.startswith("postgresql+psycopg://")


def test_metadata_contains_tenant_tables() -> None:
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_models_can_create_schema_in_sqlite() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")

    try:
        Base.metadata.create_all(engine)

        assert set(inspect(engine).get_table_names()) == EXPECTED_TABLES
    finally:
        engine.dispose()
