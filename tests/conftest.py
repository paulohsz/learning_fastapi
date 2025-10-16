from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import get_session
from app.main import app
from app.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite+pysqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # engine = create_engine(
    #       "sqlite+pysqlite:///:memory:",
    #       echo=True,
    #       future=True
    #   )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        # Ensure the session is properly closed
        session.close()

    # Clean up all tables
    table_registry.metadata.drop_all(engine)

    # Close all connections in the pool
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 9, 26, 12, 30, 15)):
    def fake_time_hook(mapper, connection, target):
        # Set the created_at field to our fixed time
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    user = User(username='john.doe', email='john.doe@example.com', password='secret')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
