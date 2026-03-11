import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

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
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error(f"Error de la API: {response.json().get('error_description', 'Desconocido')}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return None

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")

    with st.expander("🌐 Accesibilidad e Inclusión", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", ["Español", "Português", "English", "Náhuatl", "Maya"])
        lectura_facil_on = st.toggle("Modo Lectura Fácil", help="Aumenta el tamaño de letra significativamente.")
        contraste_alto_on = st.toggle("Modo Alto Contraste", help="Colores blanco y negro de alta visibilidad.")

    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Cuánto ganas por cada peso invertido.")
        st.write("**AIO:** SEO optimizado para Inteligencia Artificial.")

    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube"):
        st.link_button("1. Autorizar en Tiendanube", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers")
        temp_code = st.text_input("2. Pega el 'Code' aquí:")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state['api_token'] = token
                st.success("¡Conexión Real Establecida! ✅")

    st.divider()
    whatsapp_on = st.toggle("WhatsApp", value=True)
    sms_on = st.toggle("SMS (Zonas sin datos)", value=False)
    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token", type="password", value=api_token_val)

# --- LÓGICA DE ESTILOS (Aquí está la magia que faltaba) ---
css_lectura_facil = """
    html, body, [class*="st-"] { font-size: 1.4rem !important; line-height: 2 !important; }
    h1 { font-size: 5rem !important; }
    p, li { font-size: 1.5rem !important; font-weight: 500 !important; }
""" if lectura_facil_on else ""

css_alto_contraste = """
    .stApp { background: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; }
    .stMetricValue { color: #FFFF00 !important; }
    .problem-box { background: #222222 !important; border: 2px solid white !important; }
    .team-card-large { background: #222222 !important; border: 2px solid white !important; }
    button { background: #FFFFFF !important; color: #000000 !important; border: 2px solid #FFFF00 !important; }
""" if contraste_alto_on else ""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ font-family: 'Inter', sans-serif; background: radial-gradient(circle at top right, #ffffff, #f1f4f9); }}
    
    /* Estilos dinámicos de los toggles */
    {css_lectura_facil}
    {css_alto_contraste}

    /* Botones y Títulos Estándar */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%);
        color: white; border-radius: 50px; padding: 14px 40px; font-weight: 800;
        width: 100%; box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3);
    }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    @keyframes gradient-move {{ 0% {{background-position:0% 50%}} 50% {{background-position:100% 50%}} 100% {{background-position:0% 50%}} }}
    
    .team-card-large {{
        text-align: center; padding: 35px; border-radius: 30px; background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px); border: 1px solid rgba(0, 86, 255, 0.1); margin-bottom: 25px;
    }}
    .problem-box {{
        background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.03); height: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# --- CONTENIDO ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico e Inclusivo para Vender Más en TiendaNube")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor ROI", "🧠 Estrategia", "👥 Equipo"])

with tab_dash:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "Recuperables: $2,400")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS", "4.2x")
    m_col4.metric("ERP", "98%")

    if st.button("🎯 Ejecutar Optimización Operativa"):
        with st.status("Procesando...", expanded=True) as status:
            time.sleep(1)
            status.update(label="Analizando inclusión cultural...", state="running")
            time.sleep(1)
            status.update(label="Sistema Optimizado.", state="complete")
        st.balloons()

with tab_ins:
    st.caption("🛡️ Cumplimiento WCAG 3.0 (2026).")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Ads & ROAS</h4><p>Sin sesgos algorítmicos.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>SEO Inclusivo</h4><p>Lectores de pantalla.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>Automatización</h4><p>Interfaz simplificada.</p></div>', unsafe_allow_html=True)

with tab_team:
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg")
    ]
    cols = st.columns(len(equipo))
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i]:
            st.markdown(f"""<div class="team-card-large">
                <img src="{img}" style="width:100%; border-radius:50%; border:5px solid #0056ff;">
                <br><strong>{nombre}</strong><br>{cargo}</div>""", unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | Tecnología Humana para Tod@s")
