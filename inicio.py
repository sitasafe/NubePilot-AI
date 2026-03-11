import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- CREDENCIALES TIENDANUBE ---
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
        if response.status_code == 200: return response.json().get("access_token")
    except: return None
    return None

# --- ESTILOS CSS (FRONTEND ROBUSTO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }
    
    .main-title {
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }
    @keyframes gradient-move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 50px !important; border: none !important; 
        padding: 14px 40px !important; font-weight: 800 !important; text-transform: uppercase;
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
    }

    .team-card-large {
        text-align: center; padding: 30px; border-radius: 25px;
        background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 86, 255, 0.1); box-shadow: 0px 15px 35px rgba(0,0,0,0.05);
        margin-bottom: 25px; transition: all 0.4s ease; height: 420px;
    }
    .team-card-large:hover { transform: translateY(-10px); border: 1px solid #0056ff; }

    .problem-box {
        background-color: white; padding: 25px; border-radius: 20px;
        border-left: 8px solid #0056ff; box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%; transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.divider()
    st.markdown("## ⚙️ Conectividad de App")
    
    metodo = st.radio("Método de Acceso", ["Oficial (OAuth)", "Técnico (X-Access-Token)"])
    
    if metodo == "Oficial (OAuth)":
        scopes = "read_products,write_products,read_orders,read_customers"
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope={scopes}"
        st.link_button("🔗 Autorizar App", auth_url)
        temp_code = st.text_input("Código de retorno:")
        if st.button("Vincular"):
            token = obtener_token_real(temp_code)
            if token: st.session_state['api_token'] = token
    else:
        st.info("💡 Modo experto: Extrae el token desde 'Network' en tu Admin.")
        manual_token = st.text_input("Ingresar Token Manual:", type="password")
        if st.button("Inyectar Token"):
            st.session_state['api_token'] = manual_token

    st.divider()
    st.text_input("Store ID", value="2831942")
    if st.session_state.get('api_token'):
        st.success("Conectado a Tiendanube ✅")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Inteligencia Operativa: Conectando ERP, Stock de Variantes y Estrategia AIO")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 ROI & Performance", "🧠 Estrategia e IA", "👥 Equipo 3"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Carritos Abandonados", "12", "-15% IA-Predict")
    m2.metric("Ventas Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("ROAS IA", "4.2x", "+0.5")
    m4.metric("Sincro ERP", "Holded", "98% Sync")

    st.divider()
    col_l, col_r = st.columns([2, 1])
    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He analizado tus variantes en Tiendanube. Hay una oportunidad de conversión en 'Talle M' usando los datos de stock real de tu ERP. ¿Optimizamos?")
        if st.button("🎯 Ejecutar Optimización de Variantes"):
            with st.status("Sincronizando..."):
                time.sleep(1)
                st.success("Variantes y Precios Tachados actualizados.")
    with col_r:
        st.info("💡 **Insight de Chatsell:** La IA ahora conoce el stock exacto por color y talle para informar a tus clientes.")

# --- TAB 2: ESTRATEGIA ---
with tab_ins:
    st.markdown("### 🧬 Big Data & Soluciones AIO")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Sincronía ERP</h4><p>Control de stock físico (Holded) vs Virtual (Tiendanube).</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>Optimización AIO</h4><p>Adaptamos el código Twig para ser relevante en la era de la IA.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>IA Conversacional</h4><p>Integración de datos reales para cerrar ventas en tiempo real.</p></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### 📈 Proyección de Demanda Inteligente")
    st.line_chart(pd.DataFrame(np.random.randint(100, 300, size=(15, 2)), columns=['Ventas con Impulsa IA', 'Ventas Sin IA']))

# --- TAB 3: EQUIPO COMPLETO (RESTAURADO) ---
with tab_team:
    st.markdown("### 👥 Los Cerebros Detrás de Impulsa IA")
    
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
    
    # Renderizar en filas de 4 para que se vea ordenado
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 160px; height: 160px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff; margin-bottom: 15px;">
                    <br><strong style="font-size: 1.3rem;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 700;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | Potenciado con tecnología Tiendanube")
