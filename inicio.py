import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Inteligencia de Caja", page_icon="🌊", layout="wide")

# --- CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- DICCIONARIO DE IDIOMAS ---
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
    }
}

# --- FUNCIONES API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json"}
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200: return response.json().get("access_token")
    except: return None
    return None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    idioma_interfaz = st.selectbox("Idioma", list(textos.keys()))
    lectura_facil_on = st.toggle("Lectura Fácil")
    contraste_alto = st.toggle("Alto Contraste")
    st.divider()
    temp_code = st.text_input("Code de Tiendanube:")
    if st.button("Vincular"):
        token = obtener_token_real(temp_code)
        if token: st.session_state['api_token'] = token

# --- ESTILOS ---
st.markdown(f"""
<style>
    .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem !important; font-weight: 800; }}
    .metric-card {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #0056ff; }}
</style>
""", unsafe_allow_html=True)

# --- CUERPO ---
t_act = textos.get(idioma_interfaz, textos["Español"])
st.markdown('<h1 class="main-title">🌊 NubeFlow IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

tab_dash, tab_pred, tab_team = st.tabs([t_act["tab1"], t_act["tab2"], "👥 Equipo"])

with tab_dash:
    m1, m2, m3 = st.columns(3)
    m1.metric(t_act["met1"], "$38,400 MXN", "-12%")
    m2.metric(t_act["met2"], "$12,450 MXN", "↑ 8%")
    m3.metric(t_act["met3"], "Óptima", "Seguridad")

    st.write("---")
    if st.button("⚡ Liberar Capital Ahora"):
        with st.status("Ejecutando..."):
            time.sleep(1)
        st.success("Campaña de liquidación activada en Tiendanube para generar caja inmediata.")

with tab_pred:
    st.markdown("### 🤖 Motor Predictivo")
    c1, c2 = st.columns([2, 1])
    with c1:
        chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Ventas', 'Caja'])
        st.line_chart(chart_data)
    with c2:
        st.write("**Sugerencia de Compra:**")
        st.table(pd.DataFrame({"Prod": ["Tenis", "Gorra"], "Acción": ["Comprar 20", "Exceso"]}))

with tab_team:
    st.write("Willan, Dalia, Montserrat, Jiram, Carlos, Edwing, Amarilis, Cesar.")

st.caption("NubeFlow IA | Equipo 3 | 2026")
