
import os
from typing import Optional, Dict, Any
from supabase import create_client, Client

_SUPABASE_URL = os.getenv("SUPABASE_URL")
# Prefer service role key for server-side operations; fall back to anon for local smoke tests.
_SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

_client: Optional[Client] = None

def get_client() -> Client:
    global _client
    if _client is None:
        if not _SUPABASE_URL or not _SUPABASE_KEY:
            raise RuntimeError("SUPABASE_URL / SUPABASE_* KEY missing. Populate your .env.")
        _client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
    return _client


def create_profile(email: str, full_name: str, currency: str = "INR", monthly_income: float = 0.0, risk_tolerance: int = 3) -> Dict[str, Any]:
    """Insert a new profile. Returns the inserted row.
    NOTE: When using RLS with auth.uid(), ensure 'id' aligns with the authenticated user's UUID.
    For service-role usage, letting DB generate id is fine.
    """
    client = get_client()
    payload = {
        "email": email,
        "full_name": full_name,
        "currency": currency,
        "monthly_income": monthly_income,
        "risk_tolerance": risk_tolerance,
    }
    res = client.table("profiles").insert(payload).execute()
    if res.data is None:
        raise RuntimeError(f"Insert failed: {res}")
    return res.data[0]


def upsert_monthly_state(user_id: str, month: str, **kwargs) -> Dict[str, Any]:
    """Upsert (insert or update) a monthly financial state.
    'month' should be YYYY-MM-01 (first day of month).
    Example: upsert_monthly_state(user_id, "2025-08-01", income=50000, expenses_fixed=12000)
    """
    client = get_client()
    payload = {"user_id": user_id, "month": month}
    payload.update(kwargs)
    res = client.table("financial_states").upsert(payload).execute()
    if res.data is None:
        raise RuntimeError(f"Upsert failed: {res}")
    return res.data[0]


def get_latest_state(user_id: str) -> Optional[Dict[str, Any]]:
    client = get_client()
    res = client.table("financial_states").select("*").eq("user_id", user_id).order("month", desc=True).limit(1).execute()
    if res.data:
        return res.data[0]
    return None
