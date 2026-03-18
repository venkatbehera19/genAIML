from fastapi import FastAPI
from app.api.user_routes import router
from app.core.logger import logger
from app.core.middleware import LoggingMiddleware

app = FastAPI(title="Async User API")

app.add_middleware(LoggingMiddleware)

@app.get('/')
def health():
  logger.info("🚀 Application started")
  return { "status": 'ok' }

app.include_router(router)