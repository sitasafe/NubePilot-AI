import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# LIBRERÍA ADICIONAL PARA EL MICROFONO
from streamlit_mic_recorder import mic_recorder

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
            st.error(f"Error de la API: {response.json().get('error_description', 'Desconocido')}")
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
        st.write("**ROAS:** Retorno de inversión publicitaria.")
        st.write("**AIO:** Optimización para Inteligencia Artificial.")

    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        temp_code = st.text_input("2. Pega el 'Code':")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state['api_token'] = token
                st.success("¡Conexión Exitosa! ✅")

    st.divider()
    whatsapp_on = st.toggle("WhatsApp Sync", value=True)
    
    api_token_val = st.session_state.get('api_token', "")
    st.text_input("Access Token Activo", type="password", value=api_token_val)

# --- LÓGICA DE ESTILOS DINÁMICOS Y EFECTOS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; line-height: 2 !important; } p, li, div { font-weight: 500 !important; }"
if contraste_alto:
    extra_styles += """
    .stApp { background: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    h1, h2, h3, h4, p, span, div, label { color: #FFFFFF !important; }
    .stMetricValue { color: #FFFF00 !important; }
    .problem-box, .team-card-large { background: #222222 !important; border: 2px solid white !important; }
    button { background: #FFFFFF !important; color: #000000 !important; }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp {{ 
        background: radial-gradient(circle at top right, #ffffff, #f1f4f9);
        font-family: 'Inter', sans-serif;
    }}

    /* EFECTO BOTÓN GRADIENTE ANIMADO */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; border: none !important;
        padding: 14px 40px !important; font-weight: 800 !important; text-transform: uppercase;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100% !important; box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-5px);
        box-shadow: 0px 15px 30px rgba(0, 86, 255, 0.5) !important;
    }}

    /* TÍTULO CON GRADIENTE ANIMADO */
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}

    /* TARJETAS DE EQUIPO CON HOVER */
    .team-card-large {{
        text-align: center; padding: 35px; border-radius: 30px;
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 86, 255, 0.1); box-shadow: 0px 20px 40px rgba(0,0,0,0.05);
        transition: all 0.4s ease; margin-bottom: 25px;
    }}
    .team-card-large:hover {{
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0px 30px 60px rgba(0, 86, 255, 0.15); border: 1px solid #0056ff;
    }}

    /* CAJAS DE ESTRATEGIA */
    .problem-box {{
        background-color: white; padding: 25px; border-radius: 20px;
        border-left: 8px solid #0056ff; box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%; transition: all 0.3s ease;
    }}
    .problem-box:hover {{ transform: translateX(10px); border-left: 8px solid #00c6ff; }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, #0056ff, #00c6ff) !important;
        color: white !important; border-radius: 10px;
    }}
    
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
t_act = textos[idioma_interfaz]
main_container = '<div class="lectura-facil">' if lectura_facil_on else '<div>'
st.markdown(main_container, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# Microfono
c_voz1, c_voz2 = st.columns([0.80, 0.20])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Iniciar Voz", stop_prompt="🛑 Parar", key='recorder')
    if audio: st.toast("Procesando comando...")

st.write("---")
tab_dash, tab_ins, tab_team = st.tabs([t_act["tab1"], "🧠 Estrategia y AIO", "👥 Equipo"])

with tab_dash:
    st.markdown(f"### {t_act['tab1']}")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(t_act["carrito"], "12", "Recuperables: $2,400")
    m_col2.metric(t_act["ventas"], "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS", "4.2x", "Ganas $4.2 por cada $1")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")

    st.write("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.error("🎯 **Tarea Crítica:** Tienes 12 carritos abandonados.")
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado una anomalía: el ROAS bajó pero el interés en 'sustentable' subió. ¿Sincronizamos?")
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1); status.update(label="Analizando jerga...", state="running")
                time.sleep(1); status.update(label="Sincronizando...", state="complete")
            st.balloons()
    with col_r:
        st.markdown("### 💬 Consulta IA")
        u_input = st.text_input("Pregunta:", placeholder="¿Cuál es mi producto más rentable?")
        if st.button("Analizar"): st.info("📊 **Análisis:** Tu producto 'Playera' tiene ROAS 5.1x.")

with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>ADS & ROAS</h4><p>Ajuste dinámico sin sesgos.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO / SEO</h4><p>Optimización para lectores de pantalla.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP CONNECT</h4><p>Interfaz simplificada universal.</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🧬 Big Data: Predicción")
    df_pred = pd.DataFrame({"Día": [f"D{i}" for i in range(1, 16)], "Ventas": np.random.randint(100, 250, 15)}).set_index("Día")
    st.line_chart(df_pred)

with tab_team:
    st.markdown("### 👥 Nuestro Equipo Multidisciplinario")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    for i in range(0, len(equipo), 3):
        cols = st.columns(3)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 220px; height: 220px; border-radius: 50%; object-fit: cover; border: 8px solid #0056ff; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
                    <br><strong>{nombre}</strong><br><small>{cargo}</small>
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Impulsa IA | Hackathon UTEL 2026")
