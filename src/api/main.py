from fastapi import FastAPI
from src.db.supabase_client import supabase
# chumma
app = FastAPI(title="FinAgent API", version="0.1")

@app.get("/")
def root():
    return {"message": "Welcome to FinAgent API 🚀"}

@app.get("/profiles")
def get_profiles():
    try:
        result = supabase.table("profiles").select("*").limit(5).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}
