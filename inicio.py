import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
# LIBRERÍA ADICIONAL PARA EL MICROFONO (Asegúrate de ponerla en requirements.txt)
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- DICCIONARIO DE IDIOMAS (INTEGRACIÓN) ---
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

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")

    with st.expander("🌐 Accesibilidad e Inclusión", expanded=True):
        idioma_interfaz = st.selectbox("Idioma Interfaz", ["Español", "Português", "English", "Náhuatl", "Maya"])
        lectura_facil_on = st.toggle("Modo Lectura Fácil", help="Aumenta el tamaño de letra.")
        contraste_alto = st.toggle("Modo Alto Contraste")

    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Cuánto ganas por cada peso en publicidad.")
        st.write("**AIO:** SEO optimizado para IAs.")

    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
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

    st.divider()
    whatsapp_on = st.toggle("Enviar plan a WhatsApp", value=True)
    sms_on = st.toggle("Notificaciones por SMS", value=False)

    api_token_val = st.session_state.get('api_token', "")
    api_token_input = st.text_input("Access Token", type="password", value=api_token_val)
    id_tienda = st.text_input("ID de Tienda", value="2831942")

# --- LÓGICA DE ESTILOS DINÁMICOS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; line-height: 2 !important; }"
if contraste_alto:
    extra_styles += """
    .stApp { background: #000000 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    h1, h2, h3, h4, p, span, div, label { color: #FFFFFF !important; }
    .problem-box, .team-card-large { background: #222222 !important; border: 2px solid white !important; }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }}
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; border: none !important;
        padding: 14px 40px !important; font-weight: 800 !important; width: 100% !important;
    }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    @keyframes gradient-move {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    .team-card-large {{
        text-align: center; padding: 35px; border-radius: 30px; background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px); border: 1px solid rgba(0, 86, 255, 0.1); margin-bottom: 25px;
    }}
    .problem-box {{ background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff; height: 100%; }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
t_act = textos[idioma_interfaz]
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# Grabación de Voz
c_voz1, c_voz2 = st.columns([0.80, 0.20])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Iniciar Voz", stop_prompt="🛑 Parar", key='recorder')

st.write("---")
tab_dash, tab_ins, tab_team = st.tabs([t_act["tab1"], "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown(f"### {t_act['tab1']}")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric(t_act["carrito"], "12", "Recuperables: $2,400")
    m_col2.metric(t_act["ventas"], "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS", "4.2x", "ROI Saludable")
    m_col4.metric("ERP", "98%", "Sincronizado")

    st.write("---")
    col_left, col_right = st.columns([2, 1])
    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado que las búsquedas de 'ropa sustentable' subieron. ¿Optimizamos SEO?")
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...") as status:
                time.sleep(1)
                status.update(label="Optimización Completa", state="complete")
            st.balloons()

# --- TAB 2: ESTRATEGIA ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Ads & ROAS</h4><p>Inversión dinámica.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO / SEO</h4><p>Contenido para IAs.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP Connect</h4><p>Automatización total.</p></div>', unsafe_allow_html=True)
    
    df_pred = pd.DataFrame({"Ventas": np.random.randint(100, 200, 15)}).set_index(np.arange(1, 16))
    st.line_chart(df_pred)

# --- TAB 3: EQUIPO (RESTAURADO) ---
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
    
    # Renderizado en cuadrícula de 3 columnas
    for i in range(0, len(equipo), 3):
        cols = st.columns(3)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff; margin-bottom: 20px;">
                    <br><strong style="font-size: 1.4rem;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 700;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
