from fastapi import APIRouter, status

from app.config.log_config import logger
from app.schemas.tax import  TaxRequest, TaxResponse
from app.services.tax_service import TaxService
from app.exceptions.domain import InternalServerError

router = APIRouter(prefix='/tax', tags=["tax"])

@router.post('/', status_code=status.HTTP_200_OK, response_model=TaxResponse)
async def calculate_tax(req_data: TaxRequest):
  """
  Calculates the annual income tax based on the provided salary components 
  and selected tax regime.
  """

  try:
    tax = TaxService(req_data)
    res = tax.calculate_tax()
    return res
  except Exception as e:
    logger.error("Unexpected error in list_users:", str(e))
    raise InternalServerError("An internal error occurred while calculating tax. Please try again.") from e
  