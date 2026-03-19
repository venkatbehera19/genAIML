from fastapi import FastAPI
from app.routes.user_routes import router
from app.config.log_config import logger
from app.middleware.middleware import LoggingMiddleware
from app.exceptions import AppError
from app.exceptions.handlers import app_error_handler, global_exception_handler

from app.db.database import SessionLocal, engine, Base, get_db
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async User API")

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_middleware(LoggingMiddleware)

@app.get('/')
def health():
  logger.info("🚀 Application started")
  return { "status": 'ok' }

app.include_router(router)