import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# Asegúrate de tener 'streamlit-mic-recorder' en tu requirements.txt
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Inteligencia de Caja", page_icon="🌊", layout="wide")

# --- CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- DICCIONARIO DE IDIOMAS (FOCO: CAJA E INVENTARIO) ---
textos = {
    "Español": {
        "sub": "De 5 horas de Excel a 5 minutos: Inteligencia de Caja e Inventario",
        "tab1": "📊 Dashboard NubeFlow",
        "tab2": "📈 Análisis Predictivo",
        "met1": "Capital Inmovilizado", "met2": "Ventas del Mes", "met3": "Salud de Caja"
    },
    "Português": {
        "sub": "De 5 horas de Excel para 5 minutos: Inteligência de Caixa e Inventário",
        "tab1": "📊 Dashboard NubeFlow",
        "tab2": "📈 Análise Preditiva",
        "met1": "Capital Imobilizado", "met2": "Vendas do Mês", "met3": "Saúde do Caixa"
    },
    "English": {
        "sub": "From 5 hours of Excel to 5 minutes: Cash Flow & Inventory Intelligence",
        "tab1": "📊 NubeFlow Dashboard",
        "tab2": "📈 Predictive Analysis",
        "met1": "Stuck Capital", "met2": "Monthly Sales", "met3": "Cash Health"
    },
    "Náhuatl": {
        "sub": "NubeFlow - Tehuantin ticpalehuia mo tlanamacaliz",
        "tab1": "📊 Tlanamacaliztli Monitor",
        "tab2": "📈 Tlanamacaliztli Predictivo",
        "met1": "Tochtli", "met2": "Tlanamacaliztli", "met3": "Yoliztli"
    },
    "Maya": {
        "sub": "NubeFlow - A wéet meyaj ti'al a konik ma'alob",
        "tab1": "📊 Kanáantik konol",
        "tab2": "📈 Kanáantik Predictivo",
        "met1": "Ta'akil", "met2": "Konol", "met3": "P'íit"
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
    except Exception:
        return None
    return None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.write("---")
    with st.expander("🌐 Accesibilidad", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", list(textos.keys()))
        lectura_facil_on = st.toggle("Modo Lectura Fácil")
        contraste_alto = st.toggle("Modo Alto Contraste")

    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        temp_code = st.text_input("2. Pega el 'Code' de la URL:")
        if st.button("3. Vincular Tienda"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Conexión Establecida! ✅")

    st.divider()
    api_token_val = st.session_state.get('api_token', "")
    if api_token_val:
        st.success("Tienda Conectada ✅")
    else:
        st.warning("Esperando Conexión... ⚠️")

# --- ESTILOS CSS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.3rem !important; }"
if contraste_alto:
    extra_styles += ".stApp { background: #000 !important; color: #FFF !important; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: #f8f9fc; font-family: 'Inter', sans-serif; }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800;
    }}
    .metric-card {{
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #0056ff;
    }}
    .team-card-large {{
        text-align: center; padding: 20px; border-radius: 20px;
        background: white; border: 1px solid #eee; margin-bottom: 10px;
    }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO ---
t_act = textos[idioma_interfaz]
st.markdown(f'<h1 class="main-title">🌊 NubeFlow IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# Micrófono para comandos de voz
col_v1, col_v2 = st.columns([0.8, 0.2])
with col_v2:
    audio = mic_recorder(start_prompt="🎤 Comando de Voz", stop_prompt="🛑 Parar", key='recorder')
    if audio:
        st.toast("Analizando impacto financiero...")

st.write("---")

tab_dash, tab_pred, tab_team = st.tabs([t_act["tab1"], t_act["tab2"], "👥 Equipo"])

with tab_dash:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met1"], "$38,400 MXN", "-12% (Dinero a liberar)")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met2"], "$12,450 MXN", "↑ 8%")
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(t_act["met3"], "Óptima", "Seguridad de Caja")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    c_l, c_r = st.columns([2, 1])
    with c_l:
        st.error("🚨 **Alerta de Caja:** Tienes $15,000 MXN 'atrapados' en productos de baja rotación.")
        if st.button("⚡ Liberar Capital Ahora"):
            with st.status("Ejecutando estrategia NubeFlow..."):
                time.sleep(2)
                st.success("Campaña de liquidación activada en
