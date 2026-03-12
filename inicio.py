import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Inteligencia de Caja", page_icon="🌊", layout="wide")

# --- CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- DICCIONARIO DE IDIOMAS (FOCO: FINANZAS Y CAJA) ---
textos = {
    "Español": {
        "sub": "De 5 horas de Excel a 5 minutos de IA: Salva tu flujo de caja",
        "tab1": "📊 Dashboard de Liquidez",
        "tab2": "🤖 Decisiones de Compra IA",
        "met1": "Capital Inmovilizado", "met2": "Riesgo de Quiebra (Caja)", "met3": "Ventas Perdidas (Stockout)"
    },
    "English": {
        "sub": "From 5 hours of Excel to 5 minutes of AI: Save your cash flow",
        "tab1": "📊 Liquidity Dashboard",
        "tab2": "🤖 AI Buying Decisions",
        "met1": "Stuck Capital", "met2": "Cash Flow Risk", "met3": "Missed Sales (Stockout)"
    }
}

# --- ESTILOS NUBEFLOW (Profesional y Financiero) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: #f8f9fc; font-family: 'Inter', sans-serif; }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800;
    }}
    .metric-card {{
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-bottom: 5px solid #0056ff;
    }}
    .insight-box {{
        background: #eef2ff; padding: 20px; border-radius: 15px;
        border-left: 10px solid #4f46e5; margin: 10px 0;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; font-weight: 800 !important;
        height: 3rem; width: 100%; transition: 0.3s;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    idioma = st.selectbox("🌐 Idioma", ["Español", "English"])
    st.divider()
    st.markdown("### ⚙️ Integración")
    st.success("API TiendaNube: Conectada")
    st.info("Excel Legacy: Importado")

t_act = textos[idioma]

# --- ENCABEZADO ---
st.markdown('<h1 class="main-title">🌊 NubeFlow</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])
st.markdown("> **Problem:** *Excel consume 5 horas/semana y arriesga tu liquidez.* \n> **Solution:** *Decisiones automatizadas en 5 minutos basadas en datos reales.*")

st.write("---")

# --- TABS ---
tab_dash, tab_buy, tab_team = st.tabs([t_act["tab1"], t_act["tab2"], "👥 Equipo"])

with tab_dash:
    # Métricas de Salud Financiera
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met1"], "$38,400 MXN", "-12% esta semana")
        st.write("💸 Dinero atrapado en bodega.")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met2"], "Bajo", "Saludable")
        st.write("🛡️ Tienes caja para 45 días.")
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met3"], "$2,100 MXN", "Evitables")
        st.write("⚠️ Ventas no realizadas por falta de stock.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    col_chart, col_list = st.columns([2, 1])
    with col_chart:
        st.markdown("### 📈 Predicción de Ventas vs Compra Óptima")
        d_pred = pd.DataFrame(
            np.random.randint(50, 100, size=(15, 2)),
            columns=['Demanda Estimada', 'Stock Recomendado']
        )
        st.line_chart(d_pred)
    
    with col_list:
        st.markdown("### ⚡ Acciones Rápidas")
        st.markdown('<div class="insight-box"><b>Optimizar Stock:</b> Hay 50 unidades de "Producto A" sin movimiento.</div>', unsafe_allow_html=True)
        if st.button("💰 Crear Liquidación para Flujo de Caja"):
            with st.status("Analizando API..."): time.sleep(1)
            st.success("Cupón de 'Flash Sale' creado en Tiendanube para liberar $10,000.")

with tab_buy:
    st.markdown("### 🤖 Sugerencia de Compra a Proveedores")
    st.write("Dile adiós al Excel. NubeFlow te dice exactamente qué comprar para no enterrar capital.")
    
    # Simulación de tabla de compra inteligente
    df_compra = pd.DataFrame({
        "Producto": ["Tenis Runner", "Gorra Urban", "Sudadera Azul", "Calcetines Pro"],
        "Stock Actual": [2, 45, 5, 120],
        "Ventas Prox. 30 días (IA)": [25, 10, 30, 80],
        "Sugerencia NubeFlow": ["Comprar 23", "NO COMPRAR", "Comprar 25", "Vender Exceso"]
    })
    
    st.table(df_compra)
    
    st.info("💡 **Insight IA:** Si sigues la sugerencia de compra, liberarás **$12,500 MXN** de capital este mes.")
    
    if st.button("📝 Generar Orden de Compra"):
        st.toast("Generando PDF para proveedores...")
        time.sleep(1)
        st.download_button("Descargar Orden (PDF)", "Datos de compra...", file_name="NubeFlow_Orden.pdf")

with tab_team:
    st.markdown("### 👥 El equipo detrás de NubeFlow")
    # Mantenemos tu lista de equipo original
    st.write("Willan, Dalia, Montserrat, Jiram, Carlos, Edwing, Amarilis, Cesar.")

st.write("---")
st.caption("NubeFlow IA | Hackathon UTEL 2026 | Equipo 3")
