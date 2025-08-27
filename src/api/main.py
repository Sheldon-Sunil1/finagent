from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from src.db.supabase_client import (
    get_client,
    create_profile as db_create_profile,
    upsert_monthly_state as db_upsert_monthly_state,
    get_latest_state as db_get_latest_state,
)

app = FastAPI(title="FinAgent API", version="0.1")

# ---------- Pydantic models ----------
class ProfileIn(BaseModel):
    email: str
    full_name: str
    currency: str = "INR"
    monthly_income: float = 0.0
    risk_tolerance: int = 3

class ProfileOut(ProfileIn):
    id: Optional[str] = None
    created_at: Optional[str] = None

class FinancialStateIn(BaseModel):
    user_id: str = Field(..., description="UUID of the user (profiles.id)")
    # Force YYYY-MM-01 format so months sort correctly in the DB
    month: str = Field(..., pattern=r"^\d{4}-\d{2}-01$", description="YYYY-MM-01")
    income: float = 0.0
    expenses_fixed: float = 0.0
    expenses_variable: float = 0.0
    savings: float = 0.0
    investments: float = 0.0
    notes: Optional[str] = None

# ---------- Basic health ----------
@app.get("/")
def root():
    return {"status": "ok", "service": "FinAgent API"}

# ---------- Profiles ----------
@app.get("/profiles")
def list_profiles():
    client = get_client()
    res = client.table("profiles").select("*").limit(100).execute()
    return res.data or []

@app.post("/profiles", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ProfileIn):
    try:
        row = db_create_profile(**payload.model_dump())
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Financial states ----------
@app.post("/financial-states", status_code=status.HTTP_201_CREATED)
def upsert_financial_state(payload: FinancialStateIn):
    try:
        row = db_upsert_monthly_state(**payload.model_dump())
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/financial-states/latest")
def get_latest_financial_state(user_id: str):
    try:
        row = db_get_latest_state(user_id)
        if not row:
            raise HTTPException(status_code=404, detail="No monthly state found for this user.")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
