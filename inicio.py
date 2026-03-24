# --- BLOQUE DE CONEXIÓN Y CREACIÓN DE BASE DE DATOS (REPARADO) ---
from app.core.database import engine, Base

def inicializar_db_tablas():
    try:
        # Importamos dentro de la función para ROMPER el círculo vicioso
        import app.core.models 
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        st.error(f"Error al cargar base de datos: {e}")

# Ejecutamos la creación
inicializar_db_tablas()
# ------------------------------------------------------