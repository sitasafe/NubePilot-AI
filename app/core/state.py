import uuid
import datetime

import pandas as pd
import requests
import streamlit as st


@st.cache_resource
def get_http_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session


@st.cache_resource
def get_token_vault():
    # Token storage in server memory to avoid exposing raw token in session_state.
    return {}


def guardar_token_seguro(store_id, access_token):
    # Keep an in-memory token reference for fast Streamlit interactions.
    token_ref = str(uuid.uuid4())
    get_token_vault()[token_ref] = access_token

    # Persist the store linkage in the real database.
    normalized_store_id = str(store_id or "").strip()
    if normalized_store_id and access_token:
        from app.core.database import Base, SessionLocal, engine
        from app.models.store import Store

        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            existing = db.query(Store).filter(Store.store_id == normalized_store_id).first()
            if existing:
                existing.access_token = access_token
                existing.updated_at = datetime.datetime.utcnow()
            else:
                db.add(
                    Store(
                        store_id=normalized_store_id,
                        access_token=access_token,
                        updated_at=datetime.datetime.utcnow(),
                    )
                )
            db.commit()
        finally:
            db.close()

    return token_ref


def obtener_token_seguro(token_ref):
    return get_token_vault().get(token_ref) if token_ref else None


def obtener_token_ref_desde_db(store_id):
    normalized_store_id = str(store_id or "").strip()
    if not normalized_store_id:
        return None

    from app.core.database import SessionLocal
    from app.models.store import Store

    db = SessionLocal()
    try:
        store = db.query(Store).filter(Store.store_id == normalized_store_id).first()
        if not store or not store.access_token:
            return None
        token_ref = str(uuid.uuid4())
        get_token_vault()[token_ref] = store.access_token
        return token_ref
    finally:
        db.close()


def obtener_ultima_tienda_vinculada():
    from app.core.database import SessionLocal
    from app.models.store import Store

    db = SessionLocal()
    try:
        store = db.query(Store).order_by(Store.updated_at.desc()).first()
        if not store or not store.access_token:
            return None, None
        token_ref = str(uuid.uuid4())
        get_token_vault()[token_ref] = store.access_token
        return store.store_id, token_ref
    finally:
        db.close()


def inicializar_estado_app():
    if "db_inventario" not in st.session_state:
        st.session_state.db_inventario = pd.DataFrame(
            {
                "Producto": [
                    "Tenis Pro Runner",
                    "Gorra Blue Urban",
                    "Calcetín Sport",
                    "Sudadera Lino",
                ],
                "Stock": [15, 95, 45, 4],
                "Ventas_30d": [45, 10, 30, 42],
                "Ventas_7d": [11, 2, 8, 12],
                "Costo": [1200, 350, 150, 890],
            }
        )
    if "token_ref" not in st.session_state:
        st.session_state.token_ref = None
    if "tn_store_id" not in st.session_state:
        st.session_state.tn_store_id = ""
    if "tn_snapshot" not in st.session_state:
        st.session_state.tn_snapshot = None
