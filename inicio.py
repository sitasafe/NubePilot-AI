import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE CREDENCIALES TIENDANUBE (Actualizado con tus datos reales) ---
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

# --- ESTILOS CSS PERSONALIZADOS (POTENCIADOS) ---
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
    .problem-box:hover {
        background: #fdfdff;
        border-left: 8px solid #00c6ff;
        transform: translateX(10px);
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

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    
    # AGREGADO: Glosario de Inclusión (Punto 2 y 3)
    with st.expander("📘 Glosario para Humanos"):
        st.write("**ROAS:** Es cuánto dinero ganas por cada peso que pones en publicidad.")
        st.write("**AIO:** Hacer que tu tienda sea " + '"' + "amiga" + '"' + " de las IAs como ChatGPT.")
        st.write("**Insights:** Descubrimientos sobre lo que tus clientes realmente quieren.")

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
            else:
                st.error("Error en vinculación. Revisa tus credenciales.")

    # AGREGADO: Alertas WhatsApp (Punto 2)
    st.divider()
    st.markdown("### 📲 Notificaciones")
    whatsapp_on = st.toggle("Enviar plan del día a WhatsApp", value=True)

    api_token_val = st.session_state.get('api_token', "")
    api_token_input = st.text_input("Access Token de API", type="password", value=api_token_val)
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token_input:
        st.success("Conectado a TiendaNube ✅")
    else:
        st.warning("Esperando Conexión... ⚠️")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor de Crecimiento & ROI", "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD GENERAL ---
with tab_dash:
    st.markdown("### 📊 Performance & ROI Center")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    # AGREGADO: Traducción a lenguaje humano (Punto 2)
    m_col1.metric("Carritos Abandonados", "12", "Recuperables: $2,400", delta_color="normal")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS (Publicidad)", "4.2x", "Ganas $4.2 por cada $1")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # AGREGADO: La tarea más importante (Punto 4)
        st.error("🎯 **Tarea Crítica:** Tienes 12 carritos abandonados. Ejecuta la optimización para enviarles un cupón automático.")
        
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado una anomalía: el ROAS de tus campañas bajó mientras que las búsquedas de 'ropa sustentable' subieron. ¿Sincronizamos stock del ERP y optimizamos el SEO para IA?")
        
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Analizando jerga local y modismos...", state="running")
                time.sleep(1)
                status.update(label="Sincronizando inventario (Caché activo)...", state="running")
                time.sleep(1)
                status.update(label="Ajustando pujas. Resumen enviado a WhatsApp.", state="complete", expanded=False)
            st.balloons()
            st.success("### 🚀 Sistema Optimizado: Stock actualizado y Ads ajustados.")

    with col_right:
        st.markdown("### 💬 Consulta IA")
        u_input = st.text_input("Pregunta sobre Ads o Stock:", placeholder="¿Cuál es mi producto más rentable?")
        if st.button("Analizar"):
            # AGREGADO: Contexto del modelo (Punto 1)
            st.info(f"📊 **Análisis (Gemini 1.5 Pro):** Tu producto 'Playera Algodón' tiene un ROAS de 5.1x pero stock crítico en ERP (5 unidades). Sugiero reponer stock antes de escalar Ads.")

# --- TAB 2: ESTRATEGIA Y AIO ---
with tab_ins:
    # AGREGADO: Nota de ética (Punto 4)
    st.caption("🛡️ Análisis ético basado en datos públicos y cumplimiento LGPD 2026.")
    
    st.markdown("### 🧠 Soluciones Estratégicas")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ADS & ROAS</span>
            <h4>Eficiencia Publicitaria</h4>
            <p>Ajuste dinámico de inversión según el rendimiento de ventas reales.</p>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">AIO / SEO</span>
            <h4>Optimización para IA</h4>
            <p>Adaptamos tu contenido para ser la primera respuesta en buscadores de IA.</p>
            </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ERP CONNECT</span>
            <h4>Automatización Operativa</h4>
            <p>Conexión fluida con sistemas externos para control de inventario total.</p>
            </div>""", unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("### 🧬 Big Data Engine: Análisis Predictivo")
    col_big1, col_big2 = st.columns([1.5, 1])
    
    with col_big1:
        st.markdown("#### 📈 Proyección de Demanda (Próximos 15 días)")
        df_pred = pd.DataFrame({
            "Día": [f"Día {i}" for i in range(1, 16)],
            "Ventas Reales": np.random.randint(100, 200, 15),
            "Tendencia Predictiva": np.random.randint(150, 250, 15)
        }).set_index("Día")
        st.line_chart(df_pred)
        # AGREGADO: Caching (Punto 1)
        st.caption("Última actualización: hace 2 mins (Datos en caché para optimizar API).")

    with col_big2:
        st.markdown("#### 🎯 Segmentación de Audiencia")
        st.markdown("""
        <div class="big-data-stat">
            <h2 style="margin:0; color:#00c6ff;">45,280</h2>
            <p style="margin:0; font-size:0.9rem;">Perfiles Analizados</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.progress(85, text="Fidelidad de Clientes (LTV)")
        st.progress(62, text="Probabilidad de Recompra")
        st.progress(18, text="Riesgo de Abandono")
        
        if st.button("📊 Generar Reporte de Big Data"):
            st.toast("Traduciendo datos complejos a lenguaje humano...")
            time.sleep(1)
            st.download_button("Descargar Plan de Acción PDF", data="Contenido del reporte...", file_name="Plan_Impulsa_2026.txt")

    st.write("---")
    
    col_ins1, col_ins2 = st.columns([1, 1])
    with col_ins1:
        st.markdown("#### 🚩 Hoja de Ruta SEO/AIO")
        st.error("🚨 **CRÍTICO:** 3 categorías principales sin etiquetas optimizadas para IA.")
        st.warning("⚠️ **ALERTA:** Desfase de stock detectado entre ERP y TiendaNube.")
        st.info("💡 **TIP:** Activar envíos gratis aumentó conversiones un 20% en tu nicho.")

    with col_ins2:
        st.markdown("#### 📊 Sentimiento y Mercado")
        # AGREGADO: Mención a jerga local (Punto 3)
        st.caption("Análisis ajustado a modismos de MX, AR y BR.")
        data_sentimiento = pd.DataFrame({
            "Categoría": ["Atención", "Envío", "Stock", "Precio"],
            "Tu Tienda": [90, 75, 60, 85],
            "Media Competencia": [80, 82, 85, 78]
        }).set_index("Categoría")
        st.area_chart(data_sentimiento)

# --- TAB 3: EQUIPO (CORREGIDO) ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo ")
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
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
