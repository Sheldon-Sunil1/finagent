
import os
import pytest

def test_env_present():
    assert os.getenv("SUPABASE_URL"), "SUPABASE_URL missing"
    assert os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY"), "Supabase key missing"

# For live tests, you'd mock Supabase or use a test project. Placeholder below.
@pytest.mark.skip(reason="Integration test placeholder — requires live Supabase project")
def test_smoke_insert_and_fetch():
    from src.db.supabase_client import create_profile, get_latest_state, upsert_monthly_state
    profile = create_profile(email="test@example.com", full_name="Test User", monthly_income=50000)
    state = upsert_monthly_state(profile["id"], "2025-08-01", income=50000, expenses_fixed=10000, expenses_variable=5000)
    latest = get_latest_state(profile["id"])
    assert latest is not None
