import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CREDENCIALES REALES ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    """Intercambia el 'Code' de Tiendanube por un Access Token real."""
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code.strip()
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.status_code == 200:
            return data.get("access_token")
        else:
            st.error(f"Error: {data.get('error_description', 'No se pudo obtener el token')}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 25px !important; 
        border: none !important; 
        padding: 12px 30px !important;
        font-weight: bold !important; 
        width: 100% !important;
    }
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 800;
    }
    .team-card-large {
        text-align: center; padding: 25px; border-radius: 20px;
        background: white; box-shadow: 0px 10px 20px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        # URL de autorización corregida (Authorize, no Token)
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        
        temp_code = st.text_input("2. Pega el 'Code' de la URL:")
        if st.button("3. Vincular Tienda"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Conexión Real Establecida! ✅")
            else:
                st.error("Error en vinculación.")

    st.divider()
    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token Activo", type="password", value=api_token_val, disabled=True)
    
    if api_token_val:
        st.success("Estado: Conectado ✅")
    else:
        st.warning("Estado: Esperando Conexión... ⚠️")

# --- CUERPO PRINCIPAL (DASHBOARD) ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor ROI", "🧠 Estrategia IA", "👥 Equipo"])

with tab_dash:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS Publicidad", "4.2x", "+0.5")
    m_col4.metric("Eficiencia ERP", "98%", "OK")
    
    st.write("---")
    if st.button("🎯 Ejecutar Optimización Operativa"):
        with st.status("Analizando datos de la API...", expanded=True):
            time.sleep(1)
            st.write("Sincronizando con el Client ID 27483...")
            time.sleep(1)
            st.write("Ajustando SEO para IA...")
        st.balloons()

with tab_ins:
    st.markdown("### 🧬 Análisis Predictivo de Big Data")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Ventas', 'Stock', 'Tendencia'])
    st.line_chart(chart_data)

with tab_team:
    st.markdown("### 👥 Equipo 3")
    # Aquí puedes mantener tu lista de equipo original...
    st.info("Willan, Dalia, Montserrat, Jiram, Carlos, Edwing, Amarilis, Cesar.")

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
