from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

import missioncloud_value_hub.db.models  # noqa: F401
from missioncloud_value_hub.db.base import Base
from missioncloud_value_hub.db.models import (
    AppUser,
    AuditEvent,
    BusinessUnit,
    CloudAccount,
    CloudService,
    Organization,
    Role,
    Team,
    UserRole,
)
from missioncloud_value_hub.db.seed import seed_demo_tenant


@pytest.fixture
def session_factory_fixture() -> Iterator[sessionmaker[Session]]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    try:
        yield factory
    finally:
        engine.dispose()


def row_count(session: Session, model: type[Base]) -> int:
    value = session.scalar(select(func.count()).select_from(model))
    assert value is not None
    return value


def test_demo_seed_is_idempotent(
    session_factory_fixture: sessionmaker[Session],
) -> None:
    with session_factory_fixture() as session:
        first = seed_demo_tenant(session)

    with session_factory_fixture() as session:
        second = seed_demo_tenant(session)

        assert first.created is True
        assert second.created is False
        assert second.organization_id == first.organization_id

        assert row_count(session, Organization) == 1
        assert row_count(session, BusinessUnit) == 1
        assert row_count(session, Team) == 1
        assert row_count(session, CloudAccount) == 1
        assert row_count(session, CloudService) == 1
        assert row_count(session, AppUser) == 1
        assert row_count(session, Role) == 1
        assert row_count(session, UserRole) == 1
        assert row_count(session, AuditEvent) == 1
