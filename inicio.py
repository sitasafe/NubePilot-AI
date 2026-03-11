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
        letter-spacing: 1px;
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
        text-align: center; 
        padding: 35px; 
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 86, 255, 0.1);
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05); 
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }

    .problem-box {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 8px solid #0056ff;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .review-action-card {
        background: #f8faff;
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #6200ea;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    
    # MEJORA: Glosario para evitar brecha digital
    with st.expander("📖 Glosario para Humanos"):
        st.write("**ROAS:** Cuánto ganas por cada peso que gastas en publicidad.")
        st.write("**AIO:** Optimización para que la IA (como ChatGPT) recomiende tu tienda.")
        st.write("**ERP:** Sistema que controla tus inventarios y facturas automáticamente.")

    st.write("---")
    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP Business One", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        temp_code = st.text_input("2. Pega el 'Code' de la URL:")
        if st.button("3. Vincular Tienda"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Conexión Real Establecida! ✅")

    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token Activo", type="password", value=api_token_val)
    
    # MEJORA: Notificaciones de WhatsApp
    st.divider()
    st.button("📲 Recibir alertas por WhatsApp")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")
st.write("---")

tab_dash, tab_rev, tab_ins, tab_team = st.tabs(["📊 Monitor de Crecimiento & ROI", "✨ Review Intelligence", "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown("### 📊 Performance & ROI Center")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS Publicidad", "4.2x", "+0.5")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")
    st.write("---")
    col_left, col_right = st.columns([2, 1])
    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado una anomalía: el ROAS bajó pero las búsquedas de 'ropa sustentable' subieron. ¿Optimizamos?")
        if st.button("🎯 Ejecutar Optimización Operativa"):
            st.balloons()
    with col_right:
        st.info("💡 **Dato IA:** Tu 'Playera Algodón' tiene un ROAS de 5.1x. Escala inversión ahora.")

# --- TAB 2: REVIEW INTELLIGENCE ---
with tab_rev:
    st.markdown("### ✨ Review Intelligence: El Decodificador de Opiniones")
    st.info("Transformamos los comentarios en una hoja de ruta estratégica.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🛠️ LA TAREA DE HOY (Prioridad)")
        st.markdown("""
        <div class="review-action-card">
            <strong>🔴 URGENTE:</strong> "El 42% menciona 'dificultad de armado'." <br>
            <small>Tarea: Crea un video tutorial esta semana.</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("#### ⚔️ Inteligencia Competitiva")
        st.markdown("""
        <div class="review-action-card" style="border-left-color: #00c6ff;">
            <strong>⚖️ OPORTUNIDAD:</strong> Tus competidores fallan en tiempos de entrega.<br>
            <small>Acción: Resalta 'Envío en 24h' en tu publicidad actual.</small>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: ESTRATEGIA Y AIO ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Eficiencia Publicitaria</h4><p>Ajuste dinámico según ventas reales.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>Optimización para IA (AIO)</h4><p>Sé la primera respuesta en ChatGPT y Gemini.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>Automatización Operativa</h4><p>Control de inventario total vía ERP.</p></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🧬 Big Data Engine: Análisis Predictivo")
    st.line_chart(pd.DataFrame({"Ventas": np.random.randint(100, 200, 15), "Tendencia": np.random.randint
