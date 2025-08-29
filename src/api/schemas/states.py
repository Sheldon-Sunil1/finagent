from pydantic import BaseModel, Field
from typing import Optional

class FinancialStateIn(BaseModel):
    user_id: str = Field(..., description="UUID of the user (profiles.id)")
    month: str = Field(..., pattern=r"^\d{4}-\d{2}-01$", description="YYYY-MM-01")
    income: float = 0.0
    expenses_fixed: float = 0.0
    expenses_variable: float = 0.0
    savings: float = 0.0
    investments: float = 0.0
    notes: Optional[str] = None
