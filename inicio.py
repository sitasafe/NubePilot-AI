import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Flowmerce IA", page_icon="🌊", layout="wide")

# --- 2. MEMORIA DE LA APP ---
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        "Producto": ["Tenis Runner", "Gorra Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [5, 85, 40, 3],
        "Ventas_Promedio": [4.2, 0.2, 1.5, 3.8],
        "Costo": [1200, 300, 150, 850]
    })

# --- 3. ESTILOS ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; text-align: center; }
    .metric-val { font-size: 1.8rem; font-weight: bold; color: #0052D4; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("⚙️ Simulador Logístico")
    demanda = st.slider("Impulso de Demanda (IA)", 0.5, 4.0, 1.0)
    retraso_prov = st.slider("Días de Entrega Proveedor", 1, 20, 5)
    
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Conectando..."):
            time.sleep(1)
            st.session_state.inventario["Stock"] = np.random.randint(1, 100, 4)
            st.toast("¡Sincronizado!")

# --- 5. LÓGICA DE CÁLCULO (CORREGIDA) ---
df = st.session_state.inventario.copy()
df["Ventas_P"] = df["Ventas_Promedio"] * demanda
df["Autonomia"] = df["Stock"] / df["Ventas_P"]

# Calculamos métricas financieras
dinero_enterrado = df[df["Stock"] > 50].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()

# LÍNEA CORREGIDA: Sin saltos de línea extraños para evitar el SyntaxError
ventas_riesgo = df[df["Autonomia"] < retraso_prov].apply(lambda x: x["Ventas_P"] * x["Costo"], axis=1).sum()

# --- 6. INTERFAZ ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📊 Diagnóstico", "🤖 Predicción", "💡 Valor", "👥 Equipo"])

with t1:
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="card">Dinero "Enterrado"<br><span class="metric-val">${dinero_enterrado:,.0f}</span></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">Ventas en Riesgo<br><span class="metric-val" style="color:#E53935;">${ventas_riesgo:,.0f}</span></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">Salud Financiera<br><span class="metric-val" style="color:#43A047;">{max(0, 100-(retraso_prov*2))}%</span></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📉 Proyección de Flujo de Efectivo")
    chart_data = pd.DataFrame({
        "Flujo Optimizado": np.linspace(40, 140, 20) + (demanda * 10),
        "Pérdida por Stockout": np.linspace(40, 140, 20) - (retraso_prov * 3)
    })
    st.area_chart(chart_data)

with t2:
    st.subheader("🤖 Recomendaciones de Compra Automáticas")
    def recomendar(dias):
        if dias < retraso_prov: return "🚨 COMPRAR YA"
        if dias > 90: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"

    df["Acción"] = df["Autonomia"].apply(recomendar)
    st.table(df[["Producto", "Stock", "Autonomia", "Acción"]])
    
    if st.button("🚀 Ejecutar Pedidos"):
        st.balloons()
        st.success("Órdenes enviadas a Tiendanube.")

with t3:
    st.markdown("### 🎯 Diferenciador Flowmerce")
    st.write("- **Excel:** Solo te dice cuánto tienes.\n- **Flowmerce:** Te dice cuánto dinero vas a ganar o perder.")
    st.info("“No vendemos software de inventario. Vendemos decisiones inteligentes.”")

with t4:
    equipo = ["Willan A.", "Dalia R.", "Montserrat G.", "Jiram C.", "Carlos A.", "Edwing G.", "Amarilis E.", "Cesar F."]
    cols = st.columns(4)
    for i, p in enumerate(equipo):
        cols[i%4].info(f"**{p}**\n\nEquipo 3")
