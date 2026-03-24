from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./flowmerce.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ESTA ES LA PARTE QUE HEMOS AÑADIDO PARA SOLUCIONAR EL ERROR ---
def init_db():
    # Importamos los modelos aquí para evitar importaciones circulares
    # y asegurar que Base conozca las tablas antes de crearlas.
    from app.core import models 
    Base.metadata.create_all(bind=engine)

# Ejecutamos la creación de tablas al cargar el módulo
init_db()
# -------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()