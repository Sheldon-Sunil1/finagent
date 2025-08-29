from fastapi import FastAPI
from .routers import profiles, states

app = FastAPI(title="FinAgent API", version="0.1")

# include routers
app.include_router(profiles.router)
app.include_router(states.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "FinAgent API"}
