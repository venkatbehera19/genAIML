import time
from app.core.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    start_time = time.time()
    method = request.method
    url = request.url.path
    client_ip = request.client.host if request.client else "unknown"

    try:
      response = await call_next(request)
      process_time = (time.time() - start_time) * 1000

      logger.info(
        f'{client_ip} - "{method} {url}" '
        f'{response.status_code} ({process_time:.2f}ms)'
      )
      return response
    
    except Exception as e:
      process_time = (time.time() - start_time) * 1000
      logger.exception(
        f'{client_ip} - "{method} {url}" FAILED ({process_time:.2f}ms)'
      )

      raise e
