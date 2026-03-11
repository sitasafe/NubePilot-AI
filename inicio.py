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

# --- ESTILOS CSS PERSONALIZADOS ---
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

    .problem-box {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 8px solid #0056ff; box-shadow: 0px 10px 25px rgba(0,0,0,0.03);
        height: 100%; transition: 0.3s;
    }
    .problem-box:hover { transform: translateX(5px); border-left-color: #00c6ff; }

    .review-card {
        background: #f8faff; border: 1px solid #e1e8f5; padding: 15px;
        border-radius: 12px; margin-bottom: 10px; border-left: 5px solid #6200ea;
    }
    
    .team-card-large {
        text-align: center; padding: 35px; border-radius: 30px;
        background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 86, 255, 0.1); box-shadow: 0px 20px 40px rgba(0,0,0,0.05); 
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.divider()
    st.markdown("## ⚙️ Configuración")
    metodo = st.radio("Conexión", ["OAuth", "Técnico"])
    if metodo == "OAuth":
        st.link_button("Autorizar Tiendanube", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers")
        code = st.text_input("Pegue el código:")
        if st.button("Conectar"):
            tk = obtener_token_real(code)
            if tk: st.session_state['api_token'] = tk
    else:
        manual_tk = st.text_input("X-Access-Token", type="password")
        if st.button("Inyectar"): st.session_state['api_token'] = manual_tk

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Copiloto de Crecimiento & Review Intelligence para Tiendanube")

tab_dash, tab_reviews, tab_ins, tab_team = st.tabs(["📊 Dashboard ROI", "✨ Review Intelligence", "🧠 Estrategia AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Carritos Abandonados", "12", "-15% IA")
    m2.metric("Ventas Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("Sentimiento Cliente", "88%", "+5% vs Mes Ant.")
    m4.metric("Sincro Variantes", "Activo", "Holded ERP")
    
    st.write("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado stock agotado en la variante 'Talle L'. Sugiero aplicar precio tachado en 'Talle M' para redirigir el tráfico. ¿Ejecutamos?")
        st.button("🎯 Optimizar Operación")
    with col_r:
        st.info("💡 **Dato clave:** El 95% de tus clientes lee reseñas antes de pagar. Visita la pestaña **Review Intelligence**.")

# --- TAB 2: REVIEW INTELLIGENCE (NUEVA SECCIÓN) ---
with tab_reviews:
    st.markdown("### 🔍 Decodificador de Opiniones con IA")
    st.markdown("> **Propuesta de valor:** Transformamos el caos de comentarios en una hoja de ruta estratégica para superar a tu competencia.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🚩 Tus Puntos Ciegos")
        st.markdown("""
        <div class="review-card">
            <strong>🔴 URGENTE:</strong> El 42% menciona "dificultad de armado". <br>
            <em>Acción IA:</em> Generando borrador para video tutorial y FAQ.
        </div>
        <div class="review-card">
            <strong>💡 INSIGHT:</strong> Dudas recurrentes sobre impermeabilidad.<br>
            <em>Acción IA:</em> Actualizando metatags y descripción de producto.
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("#### ⚔️ Inteligencia Competitiva")
        st.markdown("""
        <div class="review-card" style="border-left-color: #00c6ff">
            <strong>⚖️ COMPARATIVA:</strong> Tu competidor directo destaca por "cremallera duradera".<br>
            <em>Tu estado:</em> 3 quejas por cierres este mes. <br>
            <strong>Acción Sugerida:</strong> Cambiar proveedor de insumo A-1.
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.markdown("#### ⚖️ Diferenciación de Mercado")
    df_comp = pd.DataFrame({
        "Característica": ["Idioma", "Complejidad", "Enfoque", "Precio"],
        "Enterprise (Kimola)": ["Inglés", "Requiere Analistas", "Dashboards abstractos", "Excluyente ($$$)"],
        "Review Intelligence": ["Nativo Español", "Lista de tareas simple", "Acciones de ejecución", "Accesible (PyME)"]
    })
    st.table(df_comp)

# --- TAB 3: ESTRATEGIA ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas AIO")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Gestión de Ofertas</h4><p>Precios tachados dinámicos según stock de variantes.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO (Search IA)</h4><p>Indexamos tu tienda para ser la respuesta #1 en ChatGPT.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP Connect</h4><p>Sincronía total de inventario físico y digital.</p></div>', unsafe_allow_html=True)
    st.line_chart(pd.DataFrame(np.random.randint(100, 250, size=(15, 1)), columns=['Proyección de Ventas IA']))

# --- TAB 4: EQUIPO (LOS 8 INTEGRANTES) ---
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
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""<div class="team-card-large">
                    <img src="{img_url}" style="width:160px;height:160px;border-radius:50%;object-fit:cover;border:5px solid #0056ff;margin-bottom:15px;">
                    <br><strong>{nombre}</strong><br><span style="color:#0056ff">{cargo}</span></div>""", unsafe_allow_html=True)

st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026")
