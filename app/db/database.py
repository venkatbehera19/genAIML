from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from app.config.log_config import logger

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app/data/sql_app.db")
# logger.info(f"Connecting to Database: {SQLALCHEMY_DATABASE_URL}")

DB_FILE_PATH = "/app/data/sql_app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:////{DB_FILE_PATH}"

db_dir = os.path.dirname(DB_FILE_PATH)
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)
    logger.info(f"Created directory: {db_dir}")

engine = create_engine(
  "sqlite:////./app/data/sql_app.db",
  connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
  """Dependency generator for database sessions.
    
  Yields:
    Session: A SQLAlchemy database session.
        
  Raises:
    SQLAlchemyError: If a database connection or execution error occurs.
  """
  db = SessionLocal()

  try:
    yield db
  except SQLAlchemyError as e:
    logger.error("Database session exception:", str(e))
    raise
  except Exception as e:
    logger.critical("Unexpected error during DB session: ", str(e))
    raise
  finally:
    db.close()
    logger.debug("Database session closed.")