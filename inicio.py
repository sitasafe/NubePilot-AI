import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

# --- CREDENCIALES ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- ESTILOS NUBEFLOW (Premium & Financial) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #f4f7fb; font-family: 'Inter', sans-serif; }
    .main-title {
        background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important; font-weight: 800; margin-bottom: 0;
    }
    .card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #4364F7;
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #0052D4; }
    .status-tag {
        padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: 700;
        background: #e1f5fe; color: #01579b;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS SIMULADOS ---
def get_predictive_data():
    dias = pd.date_range(start='2026-03-12', periods=30)
    ventas = np.random.normal(5000, 1000, 30).cumsum()
    caja = ventas * 0.3 + 20000
    return pd.DataFrame({"Fecha": dias, "Ventas Estimadas": ventas, "Flujo de Caja": caja}).set_index("Fecha")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.markdown("### 🌐 Configuración")
    idioma = st.selectbox("Idioma", ["Español", "English", "Português"])
    st.divider()
    st.info("💡 **Diferenciador:** NubeFlow no solo registra, predice tu liquidez.")
    st.divider()
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Conectando con API..."):
            time.sleep(1.5)
            st.success("Datos actualizados")

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 NubeFlow</h1>', unsafe_allow_html=True)
st.markdown("### **No vendas más, vende mejor.** Optimización de Caja e Inventario Predictivo.")

st.write("---")

# --- DASHBOARD PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["📊 Inteligencia de Caja", "🤖 Decisiones IA", "👥 Equipo"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("💰 **Capital Atrapado**")
        st.markdown('<p class="metric-value">$42,800 MXN</p>', unsafe_allow_html=True)
        st.caption("Dinero en stock sin movimiento (>60 días)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("⚠️ **Ventas en Riesgo**")
        st.markdown('<p class="metric-value" style="color:#e53935;">$12,300 MXN</p>', unsafe_allow_html=True)
        st.caption("Proyección de pérdida por Stockout inminente")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("🛡️ **Días de Supervivencia**")
        st.markdown('<p class="metric-value" style="color:#43a047;">45 Días</p>', unsafe_allow_html=True)
        st.caption("Salud de flujo de caja actual")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("#### 📈 Proyección Financiera (30 días)")
    st.area_chart(get_predictive_data())

with tab2:
    st.markdown("### 🤖 Centro de Decisiones NubeFlow")
    st.write("Transformamos 5 horas de Excel en 5 minutos de estrategia.")
    
    c_dec1, c_dec2 = st.columns([1.5, 1])
    
    with c_dec1:
        st.markdown("#### 🛒 Orden de Compra Sugerida")
        data_compra = {
            "Producto": ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"],
            "Velocidad Venta": ["Alta", "Nula", "Media", "Crítica"],
            "Decisión": ["COMPRAR 35 u.", "LIQUIDAR STOCK", "MANTENER", "COMPRAR 15 u."],
            "Impacto en Caja": ["-$12,000", "+$4,500", "$0", "-$3,200"]
        }
        st.table(pd.DataFrame(data_compra))
        
        if st.button("✅ Aprobar y Enviar a Proveedores"):
            st.balloons()
            st.success("Ordenes enviadas. Capital optimizado automáticamente.")

    with c_dec2:
        st.markdown("#### ⚡ Simulador de Escenarios")
        st.write("¿Qué pasa si el proveedor se retrasa?")
        retraso = st.slider("Días de retraso del proveedor", 0, 30, 5)
        
        if retraso > 10:
            st.error(f"Peligro: Un retraso de {retraso} días causará Stockout en 5 productos estrella.")
            st.write("👉 **Sugerencia:** Aumentar stock de seguridad en 15%.")
        else:
            st.info("Escenario bajo control. No se requiere capital extra.")

        st.markdown("---")
        st.markdown("#### 🎤 Comando de Voz")
        audio = mic_recorder(start_prompt="Preguntar a NubeFlow", stop_prompt="Procesar", key='fin_rec')
        if audio:
            st.write("🤖 *Analizando voz...* '¿Cuál es mi producto con más dinero enterrado?'")
            st.warning("Respuesta: Las 'Gorras Urban Blue' tienen $4,500 MXN inmovilizados.")

with tab3:
    st.markdown("### 👥 Equipo 3 - NubeFlow")
    # Formato scannable para el equipo
    equipo = [
        "Willan Álvarez (AI Architect)", "Dalia R. (Product Manager)", 
        "Montserrat G. (Strategy)", "Jiram Cabrera (Ops)",
        "Carlos Andrés A. (Liderazgo)", "Edwing Garcia (Ventas)", 
        "Amarilis Elizabeth (Gestión)", "Cesar Augusto F. (Estrategia)"
    ]
    cols = st.columns(2)
    for i, integrante in enumerate(equipo):
        cols[i % 2].write(f"✅ {integrante}")

st.write("---")
st.caption("NubeFlow | Vendiendo Liquidez, no solo Software | Hackathon UTEL 2026")
