import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# --- 1. CONTROL DE RUTAS (CRÍTICO PARA STREAMLIT CLOUD) ---
path_root = os.path.abspath(os.path.dirname(__file__))
if path_root not in sys.path:
    sys.path.insert(0, path_root)

# Intentar agregar la carpeta app al path específicamente
app_path = os.path.join(path_root, "app")
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# --- 2. IMPORTACIONES DE MÓDULOS PROPIOS ---
from app.core.database import engine, Base
from app.core.state import (
    guardar_token_seguro,
    inicializar_estado_app,
    obtener_ultima_tienda_vinculada,
)
from app.services.tiendanube import (
    extraer_inventario_desde_snapshot,
    normalizar_store_id,
    obtener_snapshot_tiendanube,
    obtener_token_real,
)
from app.services.notifications import disparar_alerta_critica

# --- 3. INICIALIZACIÓN DE DB ---
def inicializar_db_tablas(_st):
    try:
        # Importación dinámica para evitar errores de herencia
        import app.core.models
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        _st.warning(f"Aviso de DB: {e}. La app funcionará en modo memoria.")

try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

# Ejecutar inicialización
inicializar_db_tablas(st)

# --- 4. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
        @keyframes gradient-move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .stApp { background: rgba(255, 255, 255, 0.7); background-attachment: fixed; background-size: cover; }
        .main-title { background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem !important; font-weight: 800; animation: gradient-move 3s linear infinite; }
        div[data-testid="stMetric"], .stTable, .team-card-large, div[data-testid="stExpander"] { background-color: white !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. DICCIONARIO DE TEXTOS ---
idioma = "Español" # Simplificado para la corrección
t_act = {
    "sub": "Donde los datos se convierten en ventas",
    "tab0": "🚀 Nuestra Visión", "tab1": "📊 Monitor", "tab2": "🧠 Estrategia", "tab3": "👥 Equipo",
    "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja",
    "equipo_tit": "Nuestro Equipo"
}

# --- 6. LÓGICA DE DATOS ---
inicializar_estado_app()
# Cargar datos (Demo o Real)
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30)
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 99)

# --- 7. RENDERIZADO ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.write(f"✨ {t_act['sub']}")

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[1]:
    c1, c2, c3 = st.columns(3)
    c1.metric(t_act["atrapado"], "$33,250 MXN")
    c2.metric(t_act["riesgo"], "$2,289 MXN", delta="!", delta_color="inverse")
    c3.metric(t_act["salud"], "98%")
    st.bar_chart(df.set_index("Producto")["Autonomia"])

with tabs[2]:
    st.subheader("Estrategia e Inteligencia de Datos")
    condiciones = [df["Autonomia"] < 7, df["Autonomia"] > 60]
    df["Accion"] = np.select(condiciones, ["🚨 REABASTECER", "🔥 LIQUIDAR"], default="✅ ESTABLE")
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Accion"]], use_container_width=True)
    
    if st.button("🔔 Activar Monitor de Alertas Críticas", use_container_width=True):
        en_riesgo = df[df["Accion"] == "🚨 REABASTECER"]
        if not en_riesgo.empty:
            ok, msg = disparar_alerta_critica(en_riesgo)
            if ok: st.error(msg)
        else:
            st.info("Todo estable")

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"), 
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, img) in enumerate(equipo[i:i+4]):
            with cols[j]:
                # USAMOS MARKDOWN EN LUGAR DE ST.BOLD
                st.markdown(f"""
                <div style="text-align:center; background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <img src="{img}" style="width:80px; height:80px; border-radius:50%; object-fit:cover;">
                    <p style="margin: 10px 0 0 0; font-weight: bold; color: #1E1E1E;">{nombre}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #666;">{cargo}</p>
                </div>
                """, unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")