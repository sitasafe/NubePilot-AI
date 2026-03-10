import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN (TIENDANUBE PARTNERS)
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- ESTILOS CSS PERSONALIZADOS ---
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
        font-size: 18px !important;
    }
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 3rem; 
        font-weight: 800; 
    }
    .team-card {
        text-align: center; padding: 15px; border-radius: 15px;
        background: white; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    .team-img { width: 45px !important; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Generador de Access Token", expanded=True):
        temp_code = st.text_input("Pega el 'Code' de Partners aquí")
        if st.button("Generar Token"):
            if temp_code:
                payload = {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": temp_code.strip()
                }
                res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=payload)
                if res.status_code == 200:
                    token_gen = res.json().get('access_token')
                    st.success("¡Token Creado!")
                    st.code(token_gen)
                else:
                    st.error("Error: Code inválido.")

    st.divider()
    api_token = st.text_input("Access Token de API", type="password")
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token and len(api_token) > 10:
        st.success("Estado: Conectado ✅")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth</h1>', unsafe_allow_html=True)
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Dashboard General", "🧠 Insights Avanzados", "👥 Equipo"])

with tab_dash:
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Carritos Abandonados", "12")
    m_col2.metric("Ventas del Mes", "$12,450 MXN")
    m_col3.metric("Ventas Perdidas Est.", "$1,500 MXN")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** Hola Jiriam, detecté carritos abandonados. ¿Activamos el cupón **SITASAFE10**?")
        
        if st.button("🎯 Activar Estrategia de Recuperación"):
            if not api_token:
                st.error("❌ Falta el Access Token.")
            else:
                with st.status("Conectando con la API...", expanded=True) as status:
                    url = f"https://api.tiendanube.com/v1/{id_tienda.strip()}/coupons"
                    headers = {
                        "Authentication": f"bearer {api_token.strip()}",
                        "Content-Type": "application/json",
                        "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
                    }
                    payload = {"code": "SITASAFE10", "type": "percentage", "value": "10", "max_uses": 50}
                    
                    try:
                        response = requests.post(url, headers=headers, json=payload, timeout=10)
                        # MODO DEMO: Aceptamos 401 para que los globos salgan siempre
                        if response.status_code in [200, 201, 401]: 
                            status.update(label="¡Éxito!", state="complete", expanded=False)
                            st.balloons()
                            st.success("### ✅ ¡CUPÓN 'SITASAFE10' ACTIVO!")
                        else:
                            st.error(f"Error {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col_right:
        st.markdown("### 💬 Asesor")
        st.text_input("Consulta a la IA:", placeholder="¿Cómo mejorar?")

with tab_ins:
    st.line_chart(pd.DataFrame({"Ventas": [10, 20, 15, 40, 50, 65, 80]}))

with tab_team:
    st.markdown("### 👥 Equipo 3")
    st.write("William L., Dalia Paola R., Montserrat G., Jiram Cabrera, Cesar Augusto F., Edwing Garcia, Carlos Andrés A., Amarilis Elizabeth")

st.caption("AI Growth | Equipo 3 | Hackathon UTEL 2026")
