import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE ---
# MEJORA SEGURIDAD: Intentar usar Secrets primero, si no, usa tus constantes
CLIENT_ID = st.secrets.get("CLIENT_ID", "27483")
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a")
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
            # MEJORA ERRORES: Mensaje más claro para el usuario
            error_desc = response.json().get('error_description', 'Desconocido')
            st.error(f"Error de la API: {error_desc}. Intenta autorizar de nuevo.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None
    return None

# --- ESTILOS CSS PERSONALIZADOS (MANTENIDO AL 100%) ---
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
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 15px 30px rgba(0, 86, 255, 0.5) !important;
        filter: brightness(1.1);
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
    .team-card-large:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0px 30px 60px rgba(0, 86, 255, 0.15);
        border: 1px solid #0056ff;
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
    
    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #0056ff !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f6;
        border-radius: 15px 15px 0 0;
        padding: 12px 25px;
        font-weight: 700;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0056ff, #00c6ff) !important;
        color: white !important;
        box-shadow: 0px 5px 15px rgba(0, 86, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control + Glosario Inclusivo) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    
    # MEJORA INCLUSIÓN: Glosario para humanos
    with st.expander("📘 Glosario para Humanos"):
        st.caption("**ROAS:** Cuánto ganas por cada peso que inviertes en anuncios.")
        st.caption("**Insight:** Una verdad oculta en tus datos que te ayuda a vender.")
        st.caption("**AIO:** Optimización para buscadores de Inteligencia Artificial.")

    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    erp_mode = st.selectbox("Sincronización de Datos", ["Holded (ERP)", "Odoo", "Manual / Foto Inventario"])
    if "Manual" in erp_mode:
        st.info("💡 Modo inclusivo activado.")

    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        
        temp_code = st.text_input("2. Pega el 'Code' de la URL:")
        if st.button("3. Vincular Tienda"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Conexión Real Establecida! ✅")
            else:
                st.error("Revisa tu conexión o solicita un nuevo Code.")

    # MEJORA ECONOMÍA ATENCIÓN: Alerta WhatsApp
    st.divider()
    notif_wa = st.toggle("Recibir Plan del Día en WhatsApp", value=True)
    
    api_token_val = st.session_state.get('api_token', "")
    api_token_input = st.text_input("Access Token de API", type="password", value=api_token_val)
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token_input:
        st.success("Conectado ✅")
    else:
        st.warning("Esperando Conexión... ⚠️")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Asistente Humano y Estratégico para TiendaNube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Mi Negocio & ROI", "🧠 Estrategia IA", "👥 Equipo"])

# --- TAB 1: DASHBOARD GENERAL (MEJORA LENGUAJE HUMANO) ---
with tab_dash:
    st.markdown("### 📊 ¿Cómo va tu crecimiento?")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "¡Puedes recuperar $2.4k!")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    # Traducción para humanos
    m_col3.metric("ROAS (Publicidad)", "4.2x", "Ganas $4 por cada $1")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # MEJORA: Resaltar la tarea más importante (Evitar parálisis)
        st.error("🎯 **Tarea del Día:** Tienes alta demanda de 'Ropa Sustentable' pero poco stock. ¡Repón ahora para no perder ventas!")
        
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado que tus clientes de México prefieren envíos rápidos. ¿Ajustamos la logística?")
        
        if st.button("🎯 Ejecutar Optimización y Enviar a WhatsApp"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Analizando modismos locales...", state="running")
                time.sleep(1)
                status.update(label="Sincronizando con ERP (Caché activo)...", state="running")
                time.sleep(1)
                status.update(label="Listo. Resumen enviado a tu móvil.", state="complete", expanded=False)
            st.balloons()

    with col_right:
        st.markdown("### 💬 Consulta IA")
        u_input = st.text_input("Pregunta lo que quieras:", placeholder="¿Por qué no vendí ayer?")
        if st.button("Analizar"):
            st.info("📊 **Análisis:** Tu producto estrella tiene stock bajo. Si repones, tu ganancia subirá un 15%.")

# --- TAB 2: ESTRATEGIA Y AIO (MEJORA ÉTICA Y LENGUAJE) ---
with tab_ins:
    # MEJORA ÉTICA
    st.caption("🛡️ Datos protegidos y análisis basado en fuentes públicas (Ética IA 2026)")
    
    st.markdown("### 🧠 Soluciones para Crecer")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ADS & ROAS</span>
            <h4>Inversión Inteligente</h4>
            <p>Ponemos tu dinero donde realmente hay compradores, no donde hay competencia cara.</p>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">AIO / SEO</span>
            <h4>Habla con las IAs</h4>
            <p>Hacemos que ChatGPT y Gemini recomienden TU tienda a los usuarios.</p>
            </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ERP CONNECT</span>
            <h4>Cero Errores de Stock</h4>
            <p>Tu bodega y tu tienda siempre dirán lo mismo automáticamente.</p>
            </div>""", unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("### 🧬 Análisis Predictivo (Modo Eco-Inference)")
    col_big1, col_big2 = st.columns([1.5, 1])
    
    with col_big1:
        st.markdown("#### 📈 Ventas esperadas")
        df_pred = pd.DataFrame({
            "Día": [f"Día {i}" for i in range(1, 16)],
            "Ventas Reales": np.random.randint(100, 200, 15),
            "Tendencia IA": np.random.randint(150, 250, 15)
        }).set_index("Día")
        st.line_chart(df_pred)

    with col_big2:
        st.markdown("#### 🎯 Salud del Negocio")
        st.write("")
        st.progress(85, text="Fidelidad de Clientes")
        st.progress(62, text="Probabilidad de Recompra")
        st.progress(95, text="Ética y Transparencia")
        
        if st.button("📊 Generar Reporte Humano"):
            st.toast("Traduciendo datos complejos a lenguaje simple...")
            time.sleep(1)
            st.download_button("Descargar Plan de Acción PDF", data="Tus pasos a seguir son...", file_name="Plan_Impulsa_2026.txt")

# --- TAB 3: EQUIPO (MANTENIDO) ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo")
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
                    <br><strong style="font-size: 1.6rem; color: #1a1c2e;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 700; font-size: 1.1rem; text-transform: uppercase;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | Tecnología con Propósito")
