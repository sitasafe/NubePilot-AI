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

# --- ESTILOS CSS PERSONALIZADOS (REPARADOS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #ffffff, #f1f4f9);
        font-family: 'Inter', sans-serif;
    }
    
    /* Botón */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 50px !important; 
        border: none !important; 
        padding: 14px 40px !important;
        font-weight: 800 !important; 
        text-transform: uppercase;
        width: 100% !important; 
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
        transition: all 0.4s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 15px 30px rgba(0, 86, 255, 0.5) !important;
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

    /* Estilos de Etiquetas que faltaban */
    .status-tag {
        background: #e8efff;
        color: #0056ff;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 10px;
    }

    .big-data-stat {
        background: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }

    .team-card-large {
        text-align: center; padding: 35px; border-radius: 30px;
        background: white; border: 1px solid rgba(0, 86, 255, 0.1);
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05); margin-bottom: 25px;
        transition: all 0.4s ease;
    }
    .team-card-large:hover { transform: translateY(-10px); border: 1px solid #0056ff; }

    .problem-box {
        background-color: white; padding: 25px; border-radius: 20px;
        border-left: 8px solid #0056ff; box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%; transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
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
    st.text_input("Access Token de API", type="password", value=api_token_val)

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor de Crecimiento & ROI", "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    st.markdown("### 📊 Performance & ROI Center")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("ROAS Publicidad", "4.2x", "+0.5")
    m4.metric("Eficiencia ERP", "98%", "Sincronizado")
    
    st.write("---")
    col_left, col_right = st.columns([2, 1])
    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado que las búsquedas de 'ropa sustentable' subieron. ¿Optimizamos el SEO para IA?")
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Sincronizando inventario...", state="running")
                time.sleep(1)
                status.update(label="Generando Metatags AIO...", state="complete")
            st.balloons()
            st.success("### 🚀 Sistema Optimizado.")

# --- TAB 2: ESTRATEGIA Y AIO ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="problem-box"><span class="status-tag">ADS & ROAS</span><h4>Eficiencia Publicitaria</h4><p>Inversión dinámica según ventas.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="problem-box"><span class="status-tag">AIO / SEO</span><h4>Optimización para IA</h4><p>Respuesta clave en ChatGPT/Gemini.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="problem-box"><span class="status-tag">ERP CONNECT</span><h4>Automatización Operativa</h4><p>Control de stock total.</p></div>', unsafe_allow_html=True)

    st.write("---")
    col_big1, col_big2 = st.columns([1.5, 1])
    with col_big1:
        st.markdown("#### 📈 Proyección de Demanda")
        st.line_chart(pd.DataFrame(np.random.randint(100, 250, size=(15, 2)), columns=['Real', 'Prediccion']))
    with col_big2:
        st.markdown('<div class="big-data-stat"><h2 style="color:#00c6ff;">45,280</h2><p>Perfiles Analizados</p></div>', unsafe_allow_html=True)
        st.progress(85, text="Fidelidad de Clientes")

# --- TAB 3: EQUIPO (REPARADO) ---
with tab_team:
    st.markdown("### 👥 Nuestro Equipo ")
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
                card_html = f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff; margin-bottom: 15px;">
                    <br><strong style="font-size: 1.4rem;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 700;">{cargo}</span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
