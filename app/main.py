from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.store import router as store_router
from app.core.database import Base, engine
from app.models import store as store_model  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flowmerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(store_router, prefix="/stores", tags=["stores"])


@app.get("/")
def read_root():
    return {"status": "Flowmerce Engine Online", "database": "Connected"}
