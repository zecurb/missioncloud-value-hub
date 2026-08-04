from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from missioncloud_value_hub.config import get_settings

settings = get_settings()

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

session_factory: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db_session() -> Iterator[Session]:
    """Provide one database session for a request or service operation."""

    with session_factory() as session:
        yield session
