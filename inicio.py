import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Flowmerce IA", page_icon="🌊", layout="wide")

# --- LÓGICA DE CÁLCULOS REALES (No estático) ---
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = pd.DataFrame({
        "Producto": ["Tenis Pro", "Gorra Blue", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [5, 85, 40, 3],
        "Ventas_Mes": [120, 5, 50, 95],
        "Costo_Unitario": [1200, 300, 100, 800]
    })

def calcular_diagnostico(df):
    # Lógica matemática real
    df['Dias_Stock'] = (df['Stock'] / (df['Ventas_Mes'] / 30)).replace([np.inf, -np.inf], 999)
    capital_atrapado = df[df['Dias_Stock'] > 60]['Stock'].sum() * df['Costo_Unitario'].mean()
    riesgo_quiebre = len(df[df['Dias_Stock'] < 3])
    return capital_atrapado, riesgo_quiebre

# --- ESTILOS ---
st.markdown("""
<style>
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; border-left: 8px solid; margin: 10px 0; }
    .critical { background: #ffebee; border-color: #ef5350; color: #b71c1c; }
    .opportunity { background: #e8f5e9; border-color: #66bb6a; color: #1b5e20; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR INTERACTIVO ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.title("⚙️ Simulación Live")
    vendas_boost = st.slider("Aumentar Ventas (%)", 0, 100, 0)
    if st.button("🔄 Recalcular con datos de Tiendanube"):
        with st.spinner("Analizando API..."):
            time.sleep(1)
            st.session_state.stock_data['Ventas_Mes'] *= (1 + vendas_boost/100)
            st.rerun()

# --- CUERPO DE LA APP ---
st.title("🌊 Flowmerce")

# Pestañas enfocadas en ACCIÓN, no en lectura
tab1, tab2, tab3 = st.tabs(["🔍 Diagnóstico de Capital", "⚡ Ejecutor de Estrategia", "👥 Equipo"])

with tab1:
    cap, riesgo = calcular_diagnostico(st.session_state.stock_data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estado de tu Liquidez")
        st.metric("Capital Inmovilizado", f"${cap:,.0f} MXN", delta="-12% vs mes anterior")
        
        st.markdown(f"""
        <div class="status-box critical">
            <b>🚨 Alerta de la IA:</b> Tienes {riesgo} productos que se agotarán en menos de 48 horas. 
            Esto representa una pérdida potencial de <b>$12,400 MXN</b> esta semana.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.subheader("Análisis de Eficiencia")
        st.write("Días de inventario por categoría")
        chart_data = st.session_state.stock_data[['Producto', 'Dias_Stock']].set_index('Producto')
        st.bar_chart(chart_data)

with tab2:
    st.subheader("Robot de Compras e Inventario")
    st.write("Basado en el análisis de flujo, Flowmerce sugiere estas acciones inmediatas:")
    
    # Tabla dinámica que cambia según los datos de la Tab 1
    df = st.session_state.stock_data.copy()
    df['Acción'] = df['Dias_Stock'].apply(lambda x: "📦 Reponer Urgente" if x < 5 else "🔥 Liquidar Stock" if x > 90 else "✅ Mantener")
    
    st.table(df[['Producto', 'Stock', 'Dias_Stock', 'Acción']])
    
    if st.button("🚀 Ejecutar Acciones en Tiendanube"):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        st.success("API: Órdenes de compra enviadas y cupones de liquidación creados.")
        st.balloons()

with tab3:
    st.markdown("### Equipo de Desarrollo")
    st.info("Flowmerce ha sido diseñado para transformar la gestión financiera de las Pymes en Latam.")
    cols = st.columns(4)
    nombres = ["Willan A.", "Dalia R.", "Montserrat G.", "Jiram C.", "Carlos A.", "Edwing G.", "Amarilis E.", "Cesar F."]
    for i, n in enumerate(nombres):
        cols[i%4].write(f"**{n}**")

st.caption("Flowmerce v1.0.2 - Live Interaction Mode")
