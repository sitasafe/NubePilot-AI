import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN Y MEMORIA (SESSION STATE) ---
st.set_page_config(page_title="Flowmerce IA - Live", page_icon="🌊", layout="wide")

# Inicializamos la "memoria" para que los botones funcionen
if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame({
        "Producto": ["Paleta Aurora", "Labial Mate", "Sérum Hidra", "Base Perfect"],
        "Stock": [120, 8, 45, 2],
        "Ventas_Dia": [0.5, 3.2, 1.2, 4.5],
        "Costo": [450, 180, 600, 550]
    })
if 'ejecutado' not in st.session_state:
    st.session_state.ejecutado = False

# --- 2. ESTILOS CSS ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CON CONTROLES REALES ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("🎮 Panel de Control")
    
    # Este slider cambia los cálculos en tiempo real
    impulso = st.slider("Simular Pico de Ventas", 1.0, 5.0, 1.0)
    retraso = st.slider("Retraso Logístico (Días)", 0, 20, 5)
    
    st.divider()
    # BOTÓN FUNCIONAL 1: Sincronización
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Obteniendo datos reales..."):
            time.sleep(1)
            # Cambiamos los datos aleatoriamente para demostrar que funciona
            st.session_state.datos["Stock"] = np.random.randint(0, 100, 4)
            st.toast("¡Inventario actualizado desde la API!")

# --- 4. LÓGICA DE CÁLCULO DINÁMICO ---
df = st.session_state.datos.copy()
df["Ventas_Act"] = df["Ventas_Dia"] * impulso
df["Autonomia"] = df["Stock"] / df["Ventas_Act"]
# Dinero atrapado: Stock > 50 unidades
cap_atrapado = df[df["Stock"] > 50].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()
# Ventas perdidas: Si la autonomía es menor al retraso
riesgo_quiebre = df[df["Autonomia"] < retraso].apply(lambda x: x["Ventas_Act"] * x["Costo"], axis=1).sum()

# --- 5. INTERFAZ ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Monitor Financiero", "🤖 Estrategia IA", "👥 Equipo"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Capital 'Enterrado'", f"${cap_atrapado:,.0f} MXN", "Stock estancado", delta_color="inverse")
    with c2:
        st.metric("Ventas en Riesgo", f"${riesgo_quiebre:,.0f} MXN", "Por quiebre de stock", delta_color="inverse")
    with c3:
        st.metric("Eficiencia Operativa", f"{int(100 - (retraso*2))}%")

    st.write("---")
    st.subheader("📉 Proyección de Flujo de Efectivo")
    # Gráfico reactivo a los sliders
    datos_grafico = pd.DataFrame({
        "Flujo Real": np.linspace(50000, 120000, 20) + (impulso * 5000) - (retraso * 2000)
    })
    st.area_chart(datos_grafico)

with tab2:
    st.subheader("🤖 Recomendaciones de la IA")
    
    # Tabla que reacciona a los botones
    df_vis
