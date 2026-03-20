from app.schemas.tax import TaxRequest, TaxRegime
from app.constants.app_constants import Tax
from app.config.log_config import logger

class TaxService:
  """
  Service to calculate income tax based on Indian tax regimes for FY 2025-26.
  """

  def __init__(self, request: TaxRequest):
    """Initializes the TaxService with user salary details.

    Args:
      request (TaxRequest): Pydantic model containing basic, hra, 
        other_allowances, and regime.
    """
    self.req = request

  def calculate_tax(self) -> dict:
    """Performs the full tax calculation logic.

    This includes calculating total gross income, applying the appropriate 
    standard deduction, calculating slab-based tax, and adding the 4% 
    Health and Education Cess.

    Returns:
      dict: A dictionary containing:
        - total_income (float): The gross income before deductions.
        - taxable_income (float): Income after standard deduction.
        - tax (float): The final tax amount including 4% cess.
        - regime (TaxRegime): The regime used for calculation.
    """
    income = self._total_income()
    slabs = self._get_slabs()

    #handling the standard deductions
    std_deduction  = Tax.NEW_REGIME_STANDARD_DEDUCTION.value if self.req.regime == TaxRegime.NEW else Tax.OLD_REGIME_STANDARD_DEDUCTION.value
    taxable_income = max(0, income - std_deduction)

    if taxable_income < 1200000 and self.req.regime == TaxRegime.NEW:
      tax_amount = 0.0
    else:
      tax_amount = self._calculate(slabs, taxable_income)

    return {
      "total_income": income,
      "taxable_income": taxable_income,
      "std_deduction": std_deduction,
      "tax": tax_amount,
      "regime": self.req.regime
    }

  def _total_income(self) -> float:
    """Calculates the gross total income.

    Returns:
      float: Sum of basic, hra, and other allowances.
    """
    return self.req.basic + self.req.hra + self.req.other_allowances
  
  def _get_slabs(self) -> list[tuple[float, int]]:
    """Provides the tax slabs based on the selected regime for FY 2025-26.

    Returns:
      list[tuple[float, int]]: A list of tuples where each tuple 
      contains (upper_limit, tax_rate_percentage).
    """
    if self.req.regime == TaxRegime.OLD:
      return [
        (250000, 0),
        (500000, 5),
        (1000000, 20),
        (float('inf'), 30)
      ]
    else:
      return [
        (400000, 0),
        (800000, 5),
        (1200000, 10),
        (1600000, 15),
        (2000000, 20),
        (2400000, 25),
        (float('inf'), 30)
      ]
    
  def _calculate(self, slabs: list[tuple[float, int]], income: float) -> float:
    """Calculates the base tax amount using progressive slabs.

    Args:
      slabs (list[tuple[float, int]]): The slab structure to apply.
      income (float): The taxable income amount.

    Returns:
      float: The calculated base tax before cess or rebates.
    """
    tax = 0
    prev = 0
    for limit, rate in slabs:
      taxable = min(income, limit) - prev
      if taxable <= 0:
        break

      tax += taxable * (rate/100)
      prev = limit
    return tax
