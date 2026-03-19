from fastapi import FastAPI
from app.routes.user_routes import router
from app.config.log_config import logger
from app.middleware.middleware import LoggingMiddleware

from app.db.database import SessionLocal, engine, Base, get_db
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async User API")

app.add_middleware(LoggingMiddleware)

@app.get('/')
def health():
  logger.info("🚀 Application started")
  return { "status": 'ok' }

app.include_router(router)