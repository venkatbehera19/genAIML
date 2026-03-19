import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
  """Load and expose environment settings for the application."""

  def __init__(self) -> None:
    self.ENV: str = os.getenv("ENV")
    self.PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
    self.PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")

    self.DB_FILE_PATH: str = os.getenv("DB_FILE_PATH")
    self.SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")

settings = Settings()