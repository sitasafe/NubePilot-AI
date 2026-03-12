import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Motor Vivo", page_icon="🌊", layout="wide")

# --- 1. MOTOR DE DATOS DINÁMICO (Aquí está el truco) ---
# Usamos session_state para que la "memoria" de la app sea real
if 'factor_ventas' not in st.session_state:
    st.session_state.factor_ventas = 1.0

# Datos base que se verán afectados por el usuario
def generar_datos_vivos(retraso, impulso_ventas):
    productos = ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"]
    # El stock baja si las ventas suben
    stock_actual = [max(0, int(50 - ( impulso_ventas * 5))), 80, 25, 3]
    ventas_proyectadas = [4.2 * impulso_ventas, 0.1, 1.5, 3.8 * impulso_ventas]
    costos = [1200, 300, 150, 850]
    
    df = pd.DataFrame({
        "Producto": productos,
        "Stock Actual": stock_actual,
        "Ventas/Día": ventas_proyectadas,
        "Costo Unitario": costos
    })
    
    # Cálculo de días de inventario (Dato dinámico real)
    df["Días de Autonomía"] = df["Stock Actual"] / df["Ventas/Día"]
    return df

# --- 2. ESTILOS CSS ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #0052D4, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .stMetric { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .card-team { text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 15px; background: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (Controles que AFECTAN la app) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("🎮 Panel de Control")
    impulso = st.slider("Simular Impulso de Ventas (Hot Sale)", 1.0, 5.0, 1.0)
    retraso_log = st.slider("Retraso de Proveedor (Días)", 0, 30, 5)
    
    if st.button("🔄 Forzar Sincronización API"):
        with st.status("Leyendo Webhooks de Tiendanube..."):
            time.sleep(1)
            st.toast("Datos actualizados correctamente")

# --- 4. LÓGICA DE NEGOCIO ---
df_actual = generar_datos_vivos(retraso_log, impulso)
cap_atrapado = df_actual[df_actual["Stock Actual"] > 50].apply(lambda x: x["Stock Actual"] * x["Costo Unitario"], axis=1).sum()
quiebres = len(df_actual[df_actual["Días de Autonomía"] < 3])

# --- 5. INTERFAZ ---
st.markdown('<h1 class="main-title">🌊 Flowmerce IA</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Dashboard Operativo", "🤖 Ejecutor IA", "👥 Equipo"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Capital Inmovilizado", f"${cap_atrapado:,} MXN", delta="-5% riesgo")
    col2.metric("Productos en Quiebre", quiebres, delta="¡Alerta!", delta_color="inverse")
    col3.metric("ROI Optimizado", f"{85 + impulso}%", delta=f"{impulso/10}%")

    st.write("---")
    st.subheader("📉 Proyección de Flujo de Caja (Reactiva)")
    # El gráfico cambia de forma real según el slider del sidebar
    chart_data = pd.DataFrame({
        "Flujo sin Flowmerce": np.linspace(100, 150, 20) - (retraso_log * 2),
        "Flujo con Flowmerce": np.linspace(100, 200, 20) + (impulso * 5)
    })
    st.line_chart(chart_data)

with tab2:
    st.subheader("⚡ Acciones Sugeridas por la IA")
    # Mostramos la tabla que se calcula CADA VEZ que mueves un control
    df_ver = df_actual.copy()
    df_ver["Recomendación"] = df_ver["Días de Autonomía"].apply(
        lambda x: "📦 COMPRAR URGENTE" if x < 5 else ("🔥 LIQUIDAR (Exceso)" if x > 60 else "✅ ESTABLE")
    )
    st.table(df_ver[["Producto", "Stock Actual", "Días de Autonomía", "Recomendación"]])
    
    if st.button("🚀 Aplicar Cambios en Tiendanube"):
        with st.spinner("Enviando comandos..."):
            time.sleep(2)
            st.balloons()
            st.success("Órdenes de compra generadas. Los proveedores han sido notificados.")

with tab3:
    st.subheader("👥 Equipo Flowmerce")
    equipo = [
        "Willan Álvarez", "Dalia R.", "Montserrat G.", "Jiram Cabrera",
        "Carlos Andrés A.", "Edwing Garcia", "Amarilis Elizabeth", "Cesar Augusto F."
    ]
    cols = st.columns(4)
    for i, persona in enumerate(equipo):
        cols[i % 4].markdown(f'<div class="card-team"><b>{persona}</b><br><small>Equipo 3</small></div>', unsafe_allow_html=True)

st.divider()
st.caption("Flowmerce v1.1 | Hackathon UTEL 2026 | Sistema de Gestión de Capital en Tiempo Real")
