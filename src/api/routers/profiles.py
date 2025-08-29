from fastapi import APIRouter, HTTPException, status
from ..schemas.profiles import ProfileIn, ProfileOut
from ...db.supabase_client import (
    get_client,
    create_profile as db_create_profile,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("/")
def list_profiles():
    client = get_client()
    res = client.table("profiles").select("*").limit(100).execute()
    return res.data or []

@router.post("/", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ProfileIn):
    try:
        row = db_create_profile(**payload.model_dump())
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
