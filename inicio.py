import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Liquidez", page_icon="🌊", layout="wide")

# --- 2. MEMORIA DE LA APP (SESSION STATE) ---
if 'db_inventario' not in st.session_state:
    # Datos iniciales simulando la API de Tiendanube
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42], # Ventas totales al mes
        "Costo": [1200, 350, 150, 890]
    })

# --- 3. ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #0052D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .stMetric { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #0052D4; }
    .status-alert { padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 4. PANEL LATERAL (CONTROLES) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg") # Logo de Flowmerce
    st.header("⚙️ Simulador Logístico")
    st.write("Ajusta las variables del mercado:")
    
    f_demanda = st.slider("Impulso de Demanda (Factor)", 0.5, 4.0, 1.0, help="1.0 es normal, 2.0 es el doble de ventas")
    dias_entrega = st.slider("Días de entrega (Lead Time)", 1, 30, 7)
    
    st.divider()
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.status("Obteniendo datos reales..."):
            time.sleep(1.5)
            # Simulación de actualización de datos
            st.session_state.db_inventario["Stock"] = np.random.randint(2, 120, 4)
            st.success("¡Datos sincronizados!")

# --- 5. MOTOR DE CÁLCULO (LA LÓGICA DEL DIAGRAMA) ---
df = st.session_state.db_inventario.copy()

# Calculamos velocidad diaria (Ventas / 30 días) ajustada por el factor
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
# Calculamos Autonomía (Días que dura el stock)
df["Autonomia"] = df["Stock"] / df["V_Diaria"]

# Métricas para el Dashboard
dinero_atrapado = df[df["Autonomia"] > 60].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()
ventas_riesgo = df[df["Autonomia"] < dias_entrega].apply(lambda x: x["V_Diaria"] * x["Costo"] * 1.5, axis=1).sum()

# --- 6. INTERFAZ DE USUARIO ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>De inventario estancado a <b>flujo de efectivo inteligente</b>.</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Dashboard de Liquidez", "🤖 Decisiones IA", "👥 Equipo"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Dinero 'Atrapado'", f"${dinero_atrapado:,.2f} MXN", help="Capital en productos que no rotan")
    c2.metric("Ventas en Riesgo", f"${ventas_riesgo:,.2f} MXN", delta="¡Alerta!", delta_color="inverse")
    c3.metric("Salud de Inventario", f"{max(0, 100-(dias_entrega*2))}%")

    st.subheader("📉 Flujo de Caja Proyectado")
    grafico = pd.DataFrame({
        "Escenario Real": np.linspace(100, 250, 30) + (f_demanda * 10) - (dias_entrega * 2)
    })
    st.area_chart(grafico)

with tab2:
    st.subheader("⚡ Acciones Recomendadas")
    
    # Aplicar lógica de decisión del diagrama de flujo
    def analizar_accion(fila):
        if fila["Autonomia"] < dias_entrega:
            return "🚨 COMPRAR URGENTE"
        elif fila["Autonomia"] > 60:
            return "🔥 LIQUIDAR STOCK"
        else:
            return "✅ ESTABLE"

    df["Recomendacion"] = df.apply(analizar_accion, axis=1)
    
    # Mostrar tabla con formato
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Recomendacion"]].style.applymap(
        lambda x: "color: red;" if x == "🚨 COMPRAR URGENTE" else ("color: orange;" if x == "🔥 LIQUIDAR STOCK" else "color: green;"),
        subset=["Recomendacion"]
    ), use_container_width=True)

    if st.button("🚀 Aplicar Cambios en Tiendanube"):
        with st.spinner("Ejecutando órdenes..."):
            time.sleep(2)
            st.balloons()
            st.success("¡Estrategia aplicada con éxito!")

with tab3:
    st.subheader("EQUIPO 3 - Hackathon")
    equipo = ["Dalia R.", "César F.", "Willan Á.", "Carlos A.", "Montserrat G.", "Edwing G.", "Jiram C.", "Fernando C."]
    cols = st.columns(4)
    for i, p in enumerate(equipo):
        cols[i%4].write(f"🔹 **{p}**")

st.divider()
st.caption("Flowmerce v3.5 | Hackathon UTEL 2026")
