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

# --- DICCIONARIO DE IDIOMAS (INTEGRACIÓN ACTUALIZADA) ---
textos = {
    "Español": {
        "sub": "Tu Copiloto Estratégico e Inclusivo para Vender Más en TiendaNube",
        "tab1": "📊 Monitor de Crecimiento & ROI",
        "tab_ojo": "👁️ Ojo Nube (Visión IA)",
        "carrito": "Carritos Abandonados", "ventas": "Ventas del Mes"
    },
    "Português": {
        "sub": "Seu Copiloto Estratégico e Inclusivo para Vender Mais na TiendaNube",
        "tab1": "📊 Monitor de Crescimento e ROI",
        "tab_ojo": "👁️ Ojo Nube (Visão IA)",
        "carrito": "Carrinhos Abandonados", "ventas": "Vendas do Mês"
    },
    "English": {
        "sub": "Your Strategic and Inclusive Copilot to Sell More on TiendaNube",
        "tab1": "📊 Growth & ROI Monitor",
        "tab_ojo": "👁️ Nube Eye (AI Vision)",
        "carrito": "Abandoned Carts", "ventas": "Monthly Sales"
    },
    "Náhuatl": {
        "sub": "Itechpahuic tlanamacaliztli - Tehuantin ticpalehuia",
        "tab1": "📊 Tlanamacaliztli Monitor",
        "tab_ojo": "👁️ Ojo Nube (IA Ixtli)",
        "carrito": "Tlacualiztli", "ventas": "Tlanamacaliztli Metztli"
    },
    "Maya": {
        "sub": "A wéet meyaj ti'al a konik ma'alob ti' TiendaNube",
        "tab1": "📊 Kanáantik konol",
        "tab_ojo": "👁️ Ojo Nube (IA Wich)",
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
        lectura_facil_on = st.toggle("Modo Lectura Fácil", help="Aumenta el tamaño de letra y contraste.")
        contraste_alto = st.toggle("Modo Alto Contraste")

    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Gasto en publicidad vs retorno.")
        st.write("**Ojo Nube:** IA de visión para digitalizar facturas físicas.")

    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded", "Odoo", "Manual"])
    
    with st.expander("🔑 Conexión Oficial Tiendanube", expanded=True):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar en Tiendanube", auth_url)
        temp_code = st.text_input("2. Pega el 'Code':")
        if st.button("3. Vincular Tienda"):
            token_valido = obtener_token_real(temp_code)
            if token_valido:
                st.session_state['api_token'] = token_valido
                st.success("¡Conexión Real Establecida! ✅")

    st.divider()
    whatsapp_on = st.toggle("WhatsApp Plan del día", value=True)
    api_token_val = st.session_state.get('api_token', "")
    api_token_input = st.text_input("Access Token", type="password", value=api_token_val)
    id_tienda = st.text_input("ID Tienda", value="2831942")

# --- ESTILOS DINÁMICOS ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; }"
if contraste_alto:
    extra_styles += ".stApp { background: #000 !important; color: #FFF !important; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }}
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; padding: 14px 40px !important;
        font-weight: 800 !important; width: 100% !important;
    }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    @keyframes gradient-move {{ 0% {{ background-position: 0%; }} 100% {{ background-position: 100%; }} }}
    .team-card-large, .problem-box {{
        background: white; padding: 25px; border-radius: 20px; box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
    }}
    .vision-scanner {{ border: 3px dashed #0056ff; padding: 20px; border-radius: 15px; text-align: center; background: #f0f5ff; }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
t_act = textos[idioma_interfaz]
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])

# Micrófono
c_voz1, c_voz2 = st.columns([0.80, 0.20])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Iniciar Voz", stop_prompt="🛑 Parar", key='recorder')
    if audio: st.toast("Procesando comando de voz...")

st.write("---")

tab_dash, tab_ojo, tab_ins, tab_team = st.tabs([t_act["tab1"], t_act["tab_ojo"], "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown(f"### {t_act['tab1']}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t_act["carrito"], "12", "$2,400")
    m2.metric(t_act["ventas"], "$12,450 MXN", "↑ 12%")
    m3.metric("ROAS", "4.2x")
    m4.metric("ERP Sync", "98%")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.error("🎯 **Tarea Crítica:** 12 carritos abandonados. Ejecuta optimización.")
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Analizando..."):
                time.sleep(2)
            st.balloons()
            st.success("### Sistema Optimizado.")
    with col_r:
        st.chat_message("assistant").write("🤖 ¿Quieres que analice tu stock crítico?")

# --- TAB NUEVA: OJO NUBE (EL AGREGADO) ---
with tab_ojo:
    st.markdown("### 👁️ Ojo Nube: Inclusión Operativa con Visión IA")
    st.write("Digitaliza facturas físicas, notas de remisión o etiquetas de stock usando la cámara.")
    
    col_cam, col_res = st.columns([1, 1])
    
    with col_cam:
        st.markdown('<div class="vision-scanner">', unsafe_allow_html=True)
        img_file = st.camera_input("Escanear Documento Físico")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_res:
        if img_file:
            with st.spinner("IA analizando texto y tablas..."):
                time.sleep(2) # Simulación de procesamiento Gemini 3.0 Flash
                st.markdown("""
                <div class="problem-box">
                    <h4 style="color:#0056ff;">✅ Datos Extraídos con Éxito</h4>
                    <p><b>Proveedor:</b> Proveedor Local S.A.</p>
                    <p><b>Producto Detectado:</b> Silla de Ruedas Ergonómica</p>
                    <p><b>Cantidad:</b> 15 unidades</p>
                    <p><b>Costo Unitario:</b> $1,200 MXN</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("📥 Subir a Tiendanube automáticamente"):
                    st.toast("Sincronizando con API de Tiendanube...")
                    time.sleep(1)
                    st.success("Stock actualizado en la tienda online.")
        else:
            st.info("Apunta la cámara a una factura o nota de venta para digitalizar tu stock.")
            st.image("https://i.imgur.com/7f3c1d.png", caption="Ejemplo de procesamiento de visión")

# --- TAB 2: ESTRATEGIA ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    c1.info("Ads & ROAS")
    c2.info("AIO / SEO Inclusivo")
    c3.info("ERP Connect")
    st.line_chart(pd.DataFrame(np.random.randn(15, 2), columns=['Reales', 'Predictivas']))

# --- TAB 3: EQUIPO ---
with tab_team:
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
                    <img src="{img_url}" style="width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff;">
                    <br><strong>{nombre}</strong><br><small>{cargo}</small>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026")
