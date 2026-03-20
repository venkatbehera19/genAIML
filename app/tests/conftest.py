"""Pytest fixtures for application tests."""

import imaplib
import pytest
from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://///app/data/sql_app.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
  """Create the tables at the start of the test session."""
  Base.metadata.create_all(bind=engine)
  yield
  Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
  """Yields a fresh database session for every test."""
  connection = engine.connect()
  transaction = connection.begin()
  session = TestingSessionLocal(bind=connection)
    
  yield session
    
  session.close()
  transaction.rollback()
  connection.close()

@pytest.fixture
def client(db_session):
  """Override the get_db dependency to use the test database."""
  def override_get_db():
    try:
      yield db_session
    finally:
      pass
            
  app.dependency_overrides[get_db] = override_get_db
  with TestClient(app) as c:
    yield c
  app.dependency_overrides.clear()

ENV_VARS = [
  "SQLALCHEMY_DATABASE_URL",
  "DB_FILE_PATH",
  "PROJECT_DESCRIPTION",
  "PROJECT_VERSION",
  "PROJECT_NAME"
]

@pytest.fixture
def clear_env(monkeypatch):
  """Remove standard env vars so tests start with clean state."""
  for var in ENV_VARS:
    monkeypatch.delenv(var, raising=False)