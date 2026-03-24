from fastapi import APIRouter, UploadFile, status, File, Depends

from app.config.env_config import settings
from app.config.log_config import logger
from app.schemas.core.ingestion import IngestionRequest, IngestionResponse
from app.services.core.ingestion_service import ingestion_service
from app.schemas.core.chat import ChatRequest
from app.utils.faiss_vector_utils import FaissVectorStore

router = APIRouter(tags=["rag"])

vector_stores = FaissVectorStore()

def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
  """Create an ingestion request from an uploaded file.

  Args:
    file: File uploaded via multipart form.

  Returns:
    IngestionRequest wrapping the file.
  """
  return IngestionRequest(file=file)

# @router.post('/upload', status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
@router.post('/upload', status_code=status.HTTP_201_CREATED)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
  """ Upload a file and index it 
  
  Args:
    request: IngestionRequest with uploaded file

  Returns:
    IngestionResponse wit message, file_path and filename

  """
  file = request.file
  ingest_result = ingestion_service.save_file(file)
  chunks = ingestion_service.ingest_file(file, ingest_result)
  return {
    "message": "File Uploaded Successfully",
    "file_path": ingest_result,
    "filename": file.filename,
    "all_data": chunks
  }

@router.get('/chat', status_code=status.HTTP_200_OK)
async def conversation(request: ChatRequest):
  """Handle chat requests for the LLM
  
  Args:
    requests:ChatRequest with query.

  Returns:
    ChatResponse with llm answer.
  """
  logger.info('Logged IN')
  results = vector_stores.similarity_search(request.query)
  return {results}