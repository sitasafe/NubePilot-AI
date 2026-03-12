import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# LIBRERÍA ADICIONAL PARA EL MICROFONO
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Hackathon", page_icon="🌊", layout="wide")

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- DICCIONARIO DE IDIOMAS (INTEGRACIÓN) ---
textos = {
    "Español": {
        "sub": "De 5 horas de Excel a 5 minutos: Inteligencia de Caja e Inventario",
        "tab1": "📊 Monitor NubeFlow",
        "carrito": "Capital en Carritos", "ventas": "Caja Proyectada"
    },
    "Português": {
        "sub": "De 5 horas de Excel para 5 minutos: Inteligência de Caixa e Inventário",
        "tab1": "📊 Monitor NubeFlow",
        "carrito": "Capital em Carrinhos", "ventas": "Caixa Projetado"
    },
    "English": {
        "sub": "From 5 hours of Excel to 5 minutes: Cash Flow & Inventory Intelligence",
        "tab1": "📊 NubeFlow Monitor",
        "carrito": "Capital in Carts", "ventas": "Projected Cash"
    },
    "Náhuatl": {
        "sub": "NubeFlow - Tehuantin ticpalehuia mo tlanamacaliz",
        "tab1": "📊 Tlanamacaliztli Monitor",
        "carrito": "Tlacualiztli", "ventas": "Tlanamacaliztli Metztli"
    },
    "Maya": {
        "sub": "NubeFlow - A wéet meyaj ti'al a konik ma'alob",
        "tab1": "📊 Kanáantik konol",
        "carrito": "P'áat kóonol", "ventas": "Konol ti' le meso'"
    }
}

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "NubeFlow (socios@tiendanube.com)"}
    payload = {
        "client_id": int(CLIENT_ID),
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code.strip()
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
    except Exception as e:
        st.error(f"Error: {e}")
    return None

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.write("---")

    with st.expander("🌐 Accesibilidad", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", ["Español", "Português", "English", "Náhuatl", "Maya"])
        lectura_facil_on = st.toggle("Modo Lectura Fácil")
        contraste_alto = st.toggle("Modo Alto Contraste")

    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        if st.button("3. Vincular"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Vinculado! ✅")

    st.divider()
    api_token_val = st.session_state.get('api_token', "")
    api_token_input = st.text_input("Access Token", type="password", value=api_token_val)
    if api_token_input: st.success("Conectado ✅")

# --- ESTILOS DINÁMICOS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; }"
if contraste_alto:
    extra_styles += ".stApp { background: #000 !important; color: #FFF !important; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    .problem-box {{
        background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.03); transition: 0.3s;
    }}
    .team-card-large {{
        text-align: center; padding: 35px; border-radius: 30px; background: white;
        border: 1px solid rgba(0, 86, 255, 0.1); transition: 0.4s;
    }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
t_act = textos[idioma_interfaz]
main_container = '<div class="lectura-facil">' if lectura_facil_on else '<div>'
st.markdown(main_container, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌊 NubeFlow IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# Micrófono
c_voz1, c_voz2 = st.columns([0.80, 0.20])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Iniciar Voz", stop_prompt="🛑 Parar", key='recorder')
    if audio: st.toast("Analizando comando financiero...")

st.write("---")

tab_dash, tab_ins, tab_team = st.tabs([t_act["tab1"], "🧠 Análisis Predictivo de Compra", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown(f"### {t_act['tab1']}")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Capital Inmovilizado", "$45,200", "-15% sugerido", delta_color="normal")
    m_col2.metric(t_act["ventas"], "$120,450 MXN", "Salud de Caja: Alta")
    m_col3.metric("Días de Stock", "18 días", "Optimizado")
    m_col4.metric("Ventas Perdidas", "$2,100", "Por falta de stock")

    st.write("---")
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.error("🎯 **Acción de Caja:** Tienes $15,000 MXN en stock que no se ha movido en 60 días. ¿Liberamos este capital?")
        if st.button("⚡ Ejecutar Estrategia NubeFlow"):
            with st.status("Analizando stock y caja...", expanded=True) as s:
                time.sleep(1)
                s.update(label="Generando campaña de liquidación en Tiendanube...", state="running")
                time.sleep(1)
                s.update(label="Ajustando órdenes de compra para mañana...", state="complete")
            st.balloons()
            st.success("### 🚀 Capital Liberado: Campaña activa y órdenes optimizadas.")

    with col_r:
        st.markdown("### 💬 Consulta Financiera")
        u_input = st.text_input("Pregunta a la IA:", placeholder="¿Cuánto capital debo invertir este mes?")
        if st.button("Analizar"):
