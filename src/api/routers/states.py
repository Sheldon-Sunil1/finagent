from fastapi import APIRouter, HTTPException, status
from ..schemas.states import FinancialStateIn
from ...db.supabase_client import (
    upsert_monthly_state as db_upsert_monthly_state,
    get_latest_state as db_get_latest_state,
)

router = APIRouter(prefix="/financial-states", tags=["Financial States"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def upsert_financial_state(payload: FinancialStateIn):
    try:
        row = db_upsert_monthly_state(**payload.model_dump())
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/latest")
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
