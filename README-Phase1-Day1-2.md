
# FinAgent — Phase 1 (Day 1-2): Database & Connection Setup

This package contains everything you need to complete **Week 1 / Day 1-2 deliverables**:
- Supabase database schema (profiles + monthly financial states)
- Python connection utilities
- Example environment variables
- Basic tests (env checks + integration test placeholder)

## 1) Create Supabase Project
1. Go to https://supabase.com/ and create a new project.
2. In **Project Settings → API**, copy:
   - Project URL
   - anon public key
   - service_role key (server-side only)
3. In **SQL Editor**, copy the contents of `schema.sql` and **Run**.

## 2) Configure Local Environment
1. Copy `.env.example` to `.env` and fill in your values.
2. (Recommended) Create a Python venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install supabase==2.* python-dotenv pytest
   ```

## 3) Try the Connection Utilities
Create a quick script (or Python REPL):
```python
from dotenv import load_dotenv; load_dotenv()
from src.db.supabase_client import create_profile, upsert_monthly_state, get_latest_state

p = create_profile(email="sheldon@example.com", full_name="Sheldon", monthly_income=65000, risk_tolerance=3)
print("Created profile:", p)

upsert_monthly_state(p["id"], "2025-08-01", income=65000, expenses_fixed=15000, expenses_variable=12000, savings_balance=50000, investments_balance=20000, cash_balance=8000)
print("Latest:", get_latest_state(p["id"]))
```

## 4) Run Tests
```bash
pytest -q
```
> Note: The integration test is skipped by default because it needs a live Supabase project.

## 5) Git Structure (suggested)
```
finagent/
  ├─ src/
  │   └─ db/
  │       └─ supabase_client.py
  ├─ tests/
  │   └─ test_db_connection.py
  ├─ schema.sql
  ├─ .env.example
  └─ README-Phase1-Day1-2.md
```

## 6) Next Steps (for Day 3-4)
- Initialize FastAPI project and define pydantic models
- Wire endpoints for profile CRUD
- Continue per the 8-week plan
