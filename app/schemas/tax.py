from pydantic import BaseModel
from enum import Enum
from typing import List

class TaxRegime(str, Enum):
  OLD = "old"
  NEW = "new"

class TaxRequest(BaseModel):
  basic: float
  hra: float
  other_allowances: float
  regime: TaxRegime = TaxRegime.NEW

class TaxResponse(BaseModel):
  total_income: float
  tax: float
  regime: str
  taxable_income: float
  std_deduction: float
  breakdown: List