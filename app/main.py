from fastapi import FastAPI

from app.api import assets

app = FastAPI()

app.include_router(assets.router, prefix="/assets", tags=["Assets"])

@app.get("/")
def read_root():
    return {"status": "OK"}


