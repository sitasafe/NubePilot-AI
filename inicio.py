import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Flowmerce IA", page_icon="🌊", layout="wide")

# --- 2. MEMORIA DE LA APP (SESSION STATE) ---
# Esto evita que los botones "no hagan nada"
if 'stock_df' not in st.session_state:
    st.session_state.stock_df = pd.DataFrame({
        "Producto": ["Paleta Aurora", "Labial Mate", "Sérum Hidra", "Base Perfect"],
        "Stock": [120, 8, 45, 2],
        "Ventas_Promedio": [0.5, 3.2, 1.2, 4.5],
        "Costo": [450, 180, 600, 550]
    })

# --- 3. ESTILOS VISUALES ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; text-align: center; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; text-align: center; }
    .metric-val { font-size: 2rem; font-weight: bold; color: #0052D4; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (CONTROLES) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("⚙️ Simulación de Mercado")
    
    # Sliders que afectan los cálculos de inmediato
    factor_demanda = st.slider("Incremento de Demanda", 1.0, 5.0, 1.0, 0.5)
    dias_retraso = st.slider("Retraso Proveedor (Días)", 0, 20, 5)
    
    st.divider()
    
    # BOTÓN FUNCIONAL 1: Sincronizar
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Conectando con API..."):
            time.sleep(1)
            # Modificamos los datos en la memoria
            st.session_state.stock_df["Stock"] = np.random.randint(5, 100, 4)
            st.success("¡Datos actualizados!")

# --- 5. LÓGICA DE NEGOCIO (CALCULOS) ---
df = st.session_state.stock_df.copy()
df["Ventas_Proyectadas"] = df["Ventas_Promedio"] * factor_demanda
df["Dias_Autonomia"] = df["Stock"] / df["Ventas_Proyectadas"]

# Capital Atrapado (Dinero en productos con mucho stock)
cap_atrapado = df[df["Stock"] > 60].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()

# Ventas en Riesgo (Si el stock se acaba antes de que llegue el pedido)
riesgo_quiebre = df[df["Dias_Autonomia"] < dias_retraso].apply(lambda x: x["Ventas_Proyectadas"] * x["Costo"], axis=1).sum()

# --- 6. INTERFAZ ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📊 Dashboard", "🤖 IA Estratégica", "🚀 El Pitch", "👥 Equipo"])

with t1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="card">Dinero "Enterrado"<br><span class="metric-val">${cap_atrapado:,.0f}</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card">Ventas en Riesgo<br><span class="metric-val" style="color:#E53935;">${riesgo_quiebre:,.0f}</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card">Salud Financiera<br><span class="metric-val" style="color:#43A047;">{max(0, 100-(dias_retraso*3))}%</span></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📉 Impacto en Flujo de Caja")
    # Gráfica que reacciona a los sliders
    chart_val = np.linspace(50000, 150000, 20) + (factor_demanda * 5000) - (dias_retraso * 2000)
    st.area_chart(pd.DataFrame(chart_val, columns=["Flujo de Efectivo"]))

with t2:
    st.subheader("🤖 Recomendaciones Automáticas")
    
    def definir_accion(dias):
        if dias < dias_retraso: return "🚨 COMPRAR YA"
        if dias > 90: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"

    df["Acción"] = df["Dias_Autonomia"].apply(definir_accion)
    
    st.table(df[["Producto", "Stock", "Dias_Autonomia", "Acción"]])
    
    # BOTÓN FUNCIONAL 2: Ejecutar
    if st.button("🚀 Ejecutar Estrategia en Tiendanube"):
        with st.status("Procesando órdenes...", expanded=True) as s:
            time.sleep(1)
            s.write("Calculando lotes óptimos...")
            time.sleep(1)
            s.update(label="¡Órdenes enviadas!", state="complete")
        st.balloons()

with t3:
    st.markdown("""
    ### 🎯 El Problema
    Las tiendas mueren por **mala gestión de inventario**. O tienen demasiado dinero atrapado en estantes, o pierden ventas por falta de stock.
    
    ### 💡 Nuestra Solución
    **Flowmerce** convierte los datos en liquidez. No solo contamos cajas; predecimos cuánto dinero vas a ganar o perder según tu inventario.
    
    > "No vendemos software de inventario. Vendemos decisiones inteligentes."
    """)

with t4:
    equipo = ["Willan A.", "Dalia R.", "Montserrat G.", "Jiram C.", "Carlos A.", "Edwing G.", "Amarilis E.", "Cesar F."]
    cols = st.columns(4)
    for i, p in enumerate(equipo):
        cols[i%4].info(f"**{p}**\n\nEquipo 3")

st.divider()
st.caption("Flowmerce v3.0 | Hackathon 2026")
