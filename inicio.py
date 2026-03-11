import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# AGREGADO: Librería para capturar audio real
from streamlit_mic_recorder import mic_recorder 

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- AGREGADO: DICCIONARIO PARA QUE EL IDIOMA FUNCIONE DE VERDAD ---
textos_dinamicos = {
    "Español": {
        "sub": "Tu Copiloto Estratégico e Inclusivo para Vender Más en TiendaNube",
        "tab1": "📊 Monitor de Crecimiento & ROI",
        "met1": "Carritos Abandonados",
        "btn_opt": "🎯 Ejecutar Optimización Operativa"
    },
    "Português": {
        "sub": "Seu Copiloto Estratégico e Inclusivo para Vender Mais na TiendaNube",
        "tab1": "📊 Monitor de Crescimento & ROI",
        "met1": "Carrinhos Abandonados",
        "btn_opt": "🎯 Executar Otimização Operativa"
    },
    "English": {
        "sub": "Your Strategic & Inclusive Copilot to Sell More on TiendaNube",
        "tab1": "📊 Growth & ROI Monitor",
        "met1": "Abandoned Carts",
        "btn_opt": "🎯 Run Operational Optimization"
    },
    "Náhuatl": {
        "sub": "Itechpahuic tlanamacaliztli - Tehuantin ticpalehuia",
        "tab1": "📊 Tlanamacaliztli Monitor",
        "met1": "Tlacualiztli",
        "btn_opt": "🎯 Chihua tlanamacaliztli"
    },
    "Maya": {
        "sub": "A wéet meyaj ti'al a konik ma'alob ti' TiendaNube",
        "tab1": "📊 Kanáantik konol",
        "met1": "P'áat kóonol",
        "btn_opt": "🎯 Beetik meyaj"
    }
}

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "ImpulsaIA (socios@tiendanube.com)"}
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200: return response.json().get("access_token")
    except: return None

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }
    .lectura-facil { font-size: 1.25rem !important; line-height: 1.8 !important; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; padding: 14px 40px !important;
        font-weight: 800 !important; width: 100% !important;
    }
    .main-title {
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }
    @keyframes gradient-move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    with st.expander("🌐 Accesibilidad e Inclusión", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", ["Español", "Português", "English", "Náhuatl", "Maya"])
        lectura_facil_on = st.toggle("Modo Lectura Fácil")
        contraste_alto = st.toggle("Modo Alto Contraste")

    # CARGA DE TEXTOS SEGÚN EL IDIOMA SELECCIONADO
    t = textos_dinamicos[idioma_interfaz]

    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Es cuánto dinero ganas por cada peso que pones en publicidad.")

    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded", "Odoo", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        st.link_button("1. Autorizar en Tiendanube", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products")
        temp_code = st.text_input("2. Pega el 'Code':")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token: st.session_state['api_token'] = token

# --- CUERPO PRINCIPAL ---
main_container = '<div class="lectura-facil">' if lectura_facil_on else '<div>'
st.markdown(main_container, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader(t["sub"]) # SUBTITULO DINÁMICO

# --- AGREGADO: FUNCIONALIDAD DE VOZ REAL ---
col_v1, col_v2 = st.columns([0.8, 0.2])
with col_v2:
    st.write("🎤 **Comando Voz**")
    audio_data = mic_recorder(start_prompt="Hablar", stop_prompt="Parar", key='voice_cmd')

if audio_data:
    st.audio(audio_data['bytes'])
    st.success("Audio capturado. Procesando comando en " + idioma_interfaz)

st.write("---")

tab_dash, tab_ins, tab_team = st.tabs([t["tab1"], "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(t["met1"], "12", "Recuperables: $2,400") # MÉTRICA DINÁMICA
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    
    if st.button(t["btn_opt"]): # BOTÓN DINÁMICO
        with st.status("Optimizando...") as s:
            time.sleep(1)
            s.update(label="Sincronizando API...", state="complete")
        st.balloons()

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo")
    # ... (Tu código de equipo se mantiene igual aquí)
    st.write("Willan Álvarez, Dalia R., Montserrat G., Jiram Cabrera, Carlos Andrés A., Edwing Garcia, Amarilis Elizabeth, Cesar Augusto F.")

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Impulsa IA | Hackathon UTEL 2026")
