from fastapi import FastAPI
from backend.app.routers import calculate, gost

app = FastAPI(title="Welding Parameters Calculator")

app.include_router(calculate.router)
app.include_router(gost.router)


@app.get("/")
def root():
    return {"message": "Welding Parameters API"}
