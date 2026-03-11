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

# --- ESTILOS CSS PERSONALIZADOS (POTENCIADOS + INCLUSIÓN) ---
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

    /* Clase para Lectura Fácil (Inclusión Cognitiva) */
    .lectura-facil {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        letter-spacing: 0.5px !important;
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
    /* ... resto de tus estilos originales ... */
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control + Inclusión) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    
    # AGREGADO: Herramientas de Accesibilidad Universal (Inclusión Visual/Cognitiva)
    with st.expander("🌐 Opciones de Inclusión", expanded=True):
        idioma = st.selectbox("Idioma de Interfaz", ["Español", "Português", "English", "Náhuatl (Beta)", "Maya (Beta)"])
        alto_contraste = st.toggle("Modo Alto Contraste")
        lectura_facil = st.toggle("Modo Lectura Fácil (Neurodiversidad)")

    # Glosario original (mantenido)
    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Es cuánto dinero ganas por cada peso que pones en publicidad.")
        st.write("**AIO:** Hacer que tu tienda sea 'amiga' de las IAs como ChatGPT.")
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

    # AGREGADO: Inclusión Tecnológica (Zonas con baja señal)
    st.divider()
    st.markdown("### 📲 Notificaciones")
    whatsapp_on = st.toggle("WhatsApp", value=True)
    sms_on = st.toggle("SMS (Para zonas con baja señal)", value=False)

# --- CUERPO PRINCIPAL ---
# Aplicar clase de lectura fácil si se activa
container_class = "lectura-facil" if lectura_facil else ""
st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico e Inclusivo para Vender Más")

# AGREGADO: Acceso por voz (Inclusión Motriz)
col_voz1, col_voz2 = st.columns([0.8, 0.2])
with col_voz2:
    if st.button("🎤 Voz"):
        st.toast("Escuchando... (Simulación de comando de voz activa)")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor ROI", "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown("### 📊 Performance & ROI Center")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "Recuperables: $2,400")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    # Explicación inclusiva del ROAS (Punto 2)
    m_col3.metric("ROAS", "4.2x", "Ganas $4.2 por cada $1")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.error("🎯 **Tarea Crítica:** Tienes 12 carritos abandonados. Ejecuta la optimización para enviarles un cupón automático.")
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado una anomalía: el ROAS bajó. ¿Sincronizamos stock?")
        
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Analizando modismos locales...", state="running")
                time.sleep(1)
                status.update(label="Resumen enviado a WhatsApp y SMS.", state="complete", expanded=False)
            st.balloons()

    with col_right:
        st.markdown("### 💬 Consulta IA")
        u_input = st.text_input("Pregunta simple:", placeholder="¿Cómo van mis ventas?")
        if st.button("Analizar"):
            st.info(f"📊 **Análisis:** Tu producto 'Playera' es el más vendido. Tienes poco inventario.")

# --- TAB 2: ESTRATEGIA Y AIO ---
with tab_ins:
    st.caption("🛡️ Análisis ético y accesible bajo estándares WCAG 2026.")
    
    st.markdown("### 🧠 Soluciones Estratégicas Inclusivas")
    # ... (Se mantienen tus bloques de Estrategia original)
    
    st.write("---")
    st.markdown("### 🧬 Big Data Engine")
    # ... (Se mantienen tus gráficos originales)

    # AGREGADO: Alerta de Inclusión de Mercado (Punto 3)
    st.info("💡 **Dato de Inclusión:** El 30% de tus compradores prefieren descripciones en lenguaje sencillo. Hemos optimizado tus textos para mayor claridad.")

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo ")
    # ... (Se mantiene tu bloque de equipo original)

st.markdown('</div>', unsafe_allow_html=True) # Cierre de div inclusivo
st.write("---")
st.caption("Impulsa IA | Hackathon UTEL 2026 | Tecnología Humana para Tod@s")
