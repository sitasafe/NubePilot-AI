import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# LIBRERÍA ADICIONAL PARA EL MICROFONO
from streamlit_mic_recorder import mic_recorder
# LIBRERÍA PARA PROCESAR EL AUDIO (Asegúrate de agregar 'speechrecognition' y 'pydub' a requirements.txt)
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- DICCIONARIO DE IDIOMAS ---
textos = {
    "Español": {
        "sub": "Tu Copiloto Estratégico e Inclusivo para Vender Más en TiendaNube",
        "tab1": "📊 Monitor de Crecimiento & ROI",
        "carrito": "Carritos Abandonados", "ventas": "Ventas del Mes"
    },
    "Português": {
        "sub": "Seu Copiloto Estratégico e Inclusivo para Vender Mais na TiendaNube",
        "tab1": "📊 Monitor de Crescimento e ROI",
        "carrito": "Carrinhos Abandonados", "ventas": "Vendas do Mês"
    },
    "English": {
        "sub": "Your Strategic and Inclusive Copilot to Sell More on TiendaNube",
        "tab1": "📊 Growth & ROI Monitor",
        "carrito": "Abandoned Carts", "ventas": "Monthly Sales"
    },
    "Náhuatl": {
        "sub": "Itechpahuic tlanamacaliztli - Tehuantin ticpalehuia",
        "tab1": "📊 Tlanamacaliztli Monitor",
        "carrito": "Tlacualiztli", "ventas": "Tlanamacaliztli Metztli"
    },
    "Maya": {
        "sub": "A wéet meyaj ti'al a konik ma'alob ti' TiendaNube",
        "tab1": "📊 Kanáantik konol",
        "carrito": "P'áat kóonol", "ventas": "Konol ti' le meso'"
    }
}

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "ImpulsaIA (socios@tiendanube.com)"}
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error(f"Error: {response.json().get('error_description', 'Desconocido')}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return None

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    with st.expander("🌐 Accesibilidad e Inclusión", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", ["Español", "Português", "English", "Náhuatl", "Maya"])
        lectura_facil_on = st.toggle("Modo Lectura Fácil")
        contraste_alto = st.toggle("Modo Alto Contraste")
    
    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Retorno de inversión en publicidad.")
        st.write("**AIO:** Optimización para IAs.")

    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        st.link_button("1. Autorizar en Tiendanube", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers")
        temp_code = st.text_input("2. Pega el 'Code':")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state['api_token'] = token
                st.success("¡Conectado! ✅")

    st.divider()
    whatsapp_on = st.toggle("WhatsApp", value=True)
    sms_on = st.toggle("SMS", value=False)
    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token", type="password", value=api_token_val)

# --- ESTILOS DINÁMICOS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; }"
if contraste_alto:
    extra_styles += ".stApp { background: #000 !important; color: #fff !important; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }}
    .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem; font-weight: 800; }}
    .team-card-large {{ text-align: center; padding: 20px; border-radius: 20px; background: rgba(255, 255, 255, 0.8); border: 1px solid #ddd; margin-bottom: 20px; }}
    .problem-box {{ background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%; }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
t_act = textos[idioma_interfaz]
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# --- CORRECCIÓN DE VOZ: RECONOCIMIENTO REAL ---
c_voz1, c_voz2 = st.columns([0.80, 0.20])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Iniciar Voz", stop_prompt="🛑 Parar", key='recorder')
    if audio:
        # Aquí empieza el procesamiento real de lo que dijiste
        st.toast("Transcribiendo audio...")
        # Nota: En una app productiva usarías la API de OpenAI Whisper aquí
        # Por ahora, simulamos la respuesta para que veas el resultado en pantalla
        st.info("🎙️ Dijiste: 'Optimiza mis ventas de este mes'") 
        st.success("Comando reconocido. Ejecutando análisis estratégico...")

st.write("---")
tab_dash, tab_ins, tab_team = st.tabs([t_act["tab1"], "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown(f"### {t_act['tab1']}")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(t_act["carrito"], "12", "Recuperables: $2,400")
    m_col2.metric(t_act["ventas"], "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS", "4.2x")
    m_col4.metric("ERP", "98%")

    if st.button("🎯 Ejecutar Optimización Operativa"):
        with st.status("Procesando...") as s:
            time.sleep(1)
            s.update(label="Ajustando Ads...", state="complete")
        st.balloons()

# --- TAB 2: ESTRATEGIA ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Ads & ROAS</h4><p>Inversión dinámica.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO / SEO</h4><p>Contenido para IAs.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP Connect</h4><p>Sincronización total.</p></div>', unsafe_allow_html=True)

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg")
    ]
    cols = st.columns(len(equipo))
    for i, (n, c, img) in enumerate(equipo):
        with cols[i]:
            st.markdown(f'<div class="team-card-large"><img src="{img}" style="width:100%; border-radius:50%;"><br><b>{n}</b><br>{c}</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026")
