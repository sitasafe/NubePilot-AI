import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Flowmerce IA", page_icon="🌊", layout="wide")

# --- 2. GESTIÓN DE MEMORIA (SESSION STATE) ---
# Esto es vital para que los botones "hagan algo" y no solo refresquen
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        "Producto": ["Tenis Runner", "Gorra Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [5, 85, 40, 3],
        "Ventas_Promedio": [4.2, 0.2, 1.5, 3.8],
        "Costo": [1200, 300, 150, 850]
    })

if 'mensaje_ia' not in st.session_state:
    st.session_state.mensaje_ia = "Haz clic en 'Sincronizar' para analizar tu tienda."

# --- 3. ESTILOS VISUALES ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; text-align: center; margin-bottom: 20px; }
    .metric-val { font-size: 1.8rem; font-weight: bold; color: #0052D4; }
    .stButton>button { width: 100%; height: 3em; background-color: #0052D4; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (CONTROLES DINÁMICOS) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("⚙️ Configuración Logística")
    
    # Sliders que recalculan todo automáticamente
    demanda = st.slider("Simular Demanda (X)", 0.5, 4.0, 1.0)
    retraso_prov = st.slider("Días de Entrega Proveedor", 1, 20, 5)
    
    st.divider()
    
    # BOTÓN 1: Sincronizar (Cambia los datos de la memoria)
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Conectando con la API..."):
            time.sleep(1.5)
            # Modificamos el stock aleatoriamente para probar la funcionalidad
            st.session_state.inventario["Stock"] = np.random.randint(1, 100, 4)
            st.session_state.mensaje_ia = "✅ Análisis completado: Se detectaron cambios en 4 SKUs."
            st.toast("¡Datos actualizados!")

# --- 5. LÓGICA DE NEGOCIO (CALCULOS EN VIVO) ---
df = st.session_state.inventario.copy()
df["Ventas_Proyectadas"] = df["Ventas_Promedio"] * demanda
df["Dias_Autonomia"] = df["Stock"] / df["Ventas_Proyectadas"]

# Capital Atrapado (Dinero en productos con exceso)
dinero_enterrado = df[df["Stock"] > 50].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()

# Ventas en Riesgo (Si el stock se acaba antes de que llegue el pedido)
ventas_riesgo = df[df["Dias_Autonomia"] < retraso_prov].apply(lambda
