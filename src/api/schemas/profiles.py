from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileIn(BaseModel):
    email: EmailStr
    full_name: str
    currency: str = "INR"
    monthly_income: float = 0.0
    risk_tolerance: int = 3

class ProfileOut(ProfileIn):
    id: Optional[str] = None
    created_at: Optional[str] = None
