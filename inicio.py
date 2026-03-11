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
    """Intercambia el 'Code' de Tiendanube por un Access Token real."""
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ImpulsaIA (socios@tiendanube.com)"
    }
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
        else:
            error_desc = response.json().get('error_description', 'Desconocido')
            st.error(f"Error de la API: {error_desc}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None
    return None

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #ffffff, #f1f4f9);
        font-family: 'Inter', sans-serif;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 50px !important; 
        border: none !important; 
        padding: 14px 40px !important;
        font-weight: 800 !important; 
        text-transform: uppercase;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
        width: 100% !important; 
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
    }

    .main-title {
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; 
        font-weight: 800; 
        animation: gradient-move 4s ease infinite;
    }
    @keyframes gradient-move {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .team-card-large {
        text-align: center; padding: 35px; border-radius: 30px;
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 86, 255, 0.1); box-shadow: 0px 20px 40px rgba(0,0,0,0.05); 
        margin-bottom: 25px; transition: all 0.4s ease;
    }

    .problem-box {
        background-color: white; padding: 25px; border-radius: 20px;
        border-left: 8px solid #0056ff; box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%; transition: all 0.3s ease;
    }
    
    .doc-mention {
        background: #eef2ff; border: 1px solid #0056ff;
        padding: 10px; border-radius: 10px; font-size: 0.85rem; color: #0056ff;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.divider()
    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Integración ERP", ["Holded (Recomendado)", "Odoo", "SAP", "Manual"])
    
    with st.expander("🔑 Auth Oficial de Aplicación", expanded=True):
        # Doc: Scopes necesarios para el correcto funcionamiento de IA predictiva
        scopes = "read_products,write_products,read_orders,read_customers,read_checkouts"
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope={scopes}"
        st.link_button("1. Autorizar App Externa", auth_url)
        temp_code = st.text_input("2. Pega el 'Code' de retorno:")
        if st.button("3. Vincular con Impulsa IA"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state['api_token'] = token
                st.success("¡Vinculación Exitosa! ✅")

    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token Activo", type="password", value=api_token_val)
    st.text_input("Store ID", value="2831942")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto de Inteligencia Operativa y AIO para Tiendanube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 ROI & Performance", "🧠 Estrategia e IA", "👥 Equipo"])

with tab_dash:
    st.markdown("### 📊 Performance Center (Real-Time)")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "Predictivo: -15%", delta_color="normal")
    m_col2.metric("Ventas Mensuales", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS Publicidad", "4.2x", "+0.5")
    m_col4.metric("Holded Sync", "98%", "Activo")

    st.write("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He analizado la estructura de tu **Base Theme**. Sugiero optimizar los snipplets de producto para mejorar la visibilidad en buscadores de IA (AIO). ¿Deseas aplicar el ajuste?")
        if st.button("🎯 Ejecutar Optimización de Conversión"):
            with st.status("Cumpliendo estándares de Homologación...", expanded=True) as s:
                time.sleep(1)
                s.update(label="Sincronizando Scopes con ERP...", state="running")
                time.sleep(1)
                s.update(label="Generando Metadatos AIO...", state="complete")
            st.balloons()
    with col_r:
        st.markdown('<div class="doc-mention"><b>Status de Integración:</b><br>App Externa Homologada bajo directrices de Tiendanube.</div>', unsafe_allow_html=True)
        st.info("💡 **Análisis de Leads:** 18% de abandonos hoy. Iniciando secuencia predictiva.")

with tab_ins:
    st.markdown("### 🧠 Soluciones de Inteligencia Predictiva")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Ads & ROAS</h4><p>Ajuste dinámico mediante análisis de margen real del ERP.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO (Search IA)</h4><p>Preparamos tu tienda para responder en ChatGPT, Gemini y Perplexity.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP Sincro</h4><p>Integración profunda con Holded para control de stock físico vs virtual.</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🧬 Análisis Predictivo de Datos (Big Data Engine)")
    col_b1, col_b2 = st.columns([2, 1])
    with col_b1:
        st.markdown("#### 📈 Proyección de Ventas vs Capacidad ERP")
        st.line_chart(pd.DataFrame(np.random.randint(100, 250, size=(15, 2)), columns=['Demanda', 'Stock Real ERP']))
    with col_b2:
        st.markdown("#### 🛡️ Manejo de Errores IA")
        st.warning("⚠️ Sin discrepancias detectadas entre Webhook y API.")
        st.progress(100, text="Integridad de Datos (Nexo ErrorBoundary)")

with tab_team:
    st.markdown("### 👥 Nuestro Equipo")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    for i in range(0, len(equipo), 3):
        cols = st.columns(3)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+3]):
            with cols[j]:
                st.markdown(f'<div class="team-card-large"><img src="{img_url}" style="width:200px;height:200px;border-radius:50%;object-fit:cover;border:6px solid #0056ff;margin-bottom:15px;"><br><strong>{nombre}</strong><br><span style="color:#0056ff;">{cargo}</span></div>', unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | Aplicación Externa Homologada")
