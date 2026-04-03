from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import store  # Importante para que detecte la tabla 'stores'

# --- ESTO CREA EL ARCHIVO flowmerce.db FÍSICAMENTE ---
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flowmerce API 🌊")

# Permitir que Streamlit se comunique con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Flowmerce Engine Online", "database": "Connected"}