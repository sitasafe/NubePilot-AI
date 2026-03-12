import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

# --- LÓGICA DE NEGOCIO (EL MOTOR) ---
def simular_tienda(impacto_ventas, retraso_logistico):
    # Datos base simulando la API de Tiendanube
    productos = ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"]
    stock_inicial = [5, 80, 25, 3]
    ventas_historicas = [4.2, 0.5, 1.5, 3.8] # Ventas promedio por día
    costo_compra = [1200, 300, 150, 850]
    
    # Aplicamos el impacto del simulador
    ventas_reales = [v * impacto_ventas for v in ventas_historicas]
    dias_autonomia = [s / v if v > 0 else 99 for s, v in zip(stock_inicial, ventas_reales)]
    
    df = pd.DataFrame({
        "Producto": productos,
        "Stock": stock_inicial,
        "Ventas/Día": ventas_reales,
        "Días Autonomía": dias_autonomia,
        "Costo": costo_compra
    })
    return df

# --- INTERFAZ Y ESTILOS ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #0052D4, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; text-align: center; }
    .stMetric { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; }
    .alert-box { padding: 15px; border-radius: 10px; margin-bottom: 10px; font-weight: 600; }
    .critical { background: #ffebee; color: #c62828; border: 1px solid #ef5350; }
    .opportunity { background: #e8f5e9; color: #2e7d32; border: 1px solid #66bb6a; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LOS CONTROLES) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("🎮 Simulador de Negocio")
    st.write("Ajusta las variables para ver cómo reacciona la IA de Flowmerce.")
    impulso = st.slider("Impulso de Demanda (Hot Sale)", 0.5, 3.0, 1.0)
    retraso = st.slider("Retraso Proveedor (Días)", 0, 30, 5)
    
    st.divider()
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.status("Analizando historial de ventas..."):
            time.sleep(1.5)
            st.success("¡Datos actualizados!")

# --- CÁLCULOS DINÁMICOS ---
df_actual = simular_tienda(impulso, retraso)
capital_atrapado = df_actual[df_actual["Días Autonomía"] > 60].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()
ventas_perdidas = df_actual[df_actual["Días Autonomía"] < retraso].apply(lambda x: (retraso - x["Días Autonomía"]) * x["Ventas/Día"] * x["Costo"] * 1.5, axis=1).sum()

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>De inventario estancado a flujo de efectivo inteligente.</b></p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard de Liquidez", "🤖 Estrategia de IA", "🚀 Pitch & Valor", "👥 Equipo"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Capital Atrapado", f"${capital_atrapado:,.0f} MXN", "Dinero durmiendo", delta_color="inverse")
    col2.metric("Riesgo Quiebre Stock", f"${ventas_perdidas:,.0f} MXN", "Ventas en riesgo", delta_color="inverse")
    col3.metric("Eficiencia de Caja", f"{max(0, 100 - (retraso*2))}%", "Salud financiera")

    st.write("---")
    st.subheader("📈 Proyección de Capital (Próximos 30 días)")
    # El gráfico cambia de verdad según el slider
    c1, c2 = st.columns([3, 1])
    with c1:
        chart_data = pd.DataFrame({
            "Flujo Proyectado": np.linspace(50000, 150000, 30) - (retraso * 1000) + (impulso * 5000)
        })
        st.area_chart(chart_data)
    with c2:
        st.markdown("#### 💡 Alerta de IA")
        if capital_atrapado > 0:
            st.markdown(f'<div class="alert-box critical">🚨 Tienes ${capital_atrapado:,.0f} inmovilizados en productos sin rotación.</div>', unsafe_allow_html=True)
        if ventas_perdidas > 0:
            st.markdown(f'<div class="alert-box critical">⚠️ Perderás ${ventas_perdidas:,.0f} si no repones stock en 48hs.</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("⚡ Motor de Órdenes Automáticas")
    
    # Lógica de decisión dinámica
    def recomendar(fila, r):
        if fila["Días Autonomía"] < r: return "🚨 COMPRA URGENTE"
        if fila["Días Autonomía"] > 90: return "🔥 LIQUIDAR (CUPÓN)"
        return "✅ MANTENER"

    df_view = df_actual.copy()
    df_view["Decisión Flowmerce"] = df_view.apply(lambda x: recomendar(x, retraso), axis=1)
    
    st.table(df_view[["Producto", "Stock", "Días Autonomía", "Decisión Flowmerce"]])
    
    if st.button("🚀 Ejecutar Decisiones en Tiendanube"):
        with st.spinner("Sincronizando con proveedores..."):
            time.sleep(2)
            st.balloons()
            st.success("Órdenes de compra enviadas. Campañas de liquidación creadas.")

with tab3:
    st.markdown("### ¿Por qué Flowmerce es disruptivo?")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**❌ El Pasado (Administrativo):**")
        st.info("Hojas de Excel, decisiones por intuición, stock muerto, capital atrapado.")
    with col_b:
        st.write("**✅ El Futuro (Estratégico):**")
        st.success("Predicción de demanda, liberación de liquidez, decisiones basadas en datos.")
    
    st.divider()
    st.markdown("> **“No vendemos software de inventario. Vendemos decisiones inteligentes que protegen el capital de las tiendas.”**")

with tab4:
    # Mostramos al equipo con un diseño limpio
    equipo = [
        ("Willan Álvarez.", "Lead Architect"), ("Dalia R.", "Product Manager"),
        ("Montserrat G.", "Strategy"), ("Jiram Cabrera", "Organización"),
        ("Carlos Andrés A.", "Liderazgo"), ("Edwing Garcia", "Ventas"),
        ("Amarilis Elizabeth", "Gestión"), ("Cesar Augusto F.", "Estrategia")
    ]
    cols = st.columns(4)
    for i, (nombre, cargo) in enumerate(equipo):
        cols[i%4].info(f"**{nombre}**\n\n{cargo}")

st.divider()
st.caption("Flowmerce Live Demo | Hackathon UTEL 2026 | Equipo 3")
