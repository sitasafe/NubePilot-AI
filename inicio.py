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

# --- FUNCIONES DE CONEXIÓN ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "ImpulsaIA (socios@tiendanube.com)"}
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200: return response.json().get("access_token")
    except: return None
    return None

# --- ESTILOS CSS ---
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
    .team-card-large {
        text-align: center; padding: 35px; border-radius: 30px; background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px); border: 1px solid rgba(0, 86, 255, 0.1); box-shadow: 0px 20px 40px rgba(0,0,0,0.05); margin-bottom: 25px;
    }
    .problem-box { background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff; height: 100%; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Panel de Control Evolucionado) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.divider()
    st.markdown("## ⚙️ Conectividad")
    
    metodo_token = st.radio("Método de Conexión", ["Oficial (OAuth)", "Técnico (X-Access-Token)"])
    
    if metodo_token == "Oficial (OAuth)":
        scopes = "read_products,write_products,read_orders,read_customers,read_checkouts"
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope={scopes}"
        st.link_button("🔗 Autorizar en Tiendanube", auth_url)
        temp_code = st.text_input("Código de retorno:")
        if st.button("Vincular Oficial"):
            token = obtener_token_real(temp_code)
            if token: st.session_state['api_token'] = token
    else:
        st.info("💡 **Tip Chatsell:** Puedes obtener este token en la pestaña 'Network' de tu admin.")
        token_manual = st.text_input("X-Access-Token manual:", type="password")
        if st.button("Vincular modo Experto"):
             st.session_state['api_token'] = token_manual
             st.success("Token manual inyectado con éxito.")

    st.divider()
    st.text_input("ID Tienda Activa", value="2831942")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Inteligencia Predictiva, Sincronización de Variantes y Gestión de Ofertas")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Performance & Ofertas", "🧠 Estrategia AIO", "👥 Equipo"])

with tab_dash:
    st.markdown("### 📊 Monitor de Inventario y Conversión")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Carritos Abandonados", "12", "Predictivo: -15%")
    m2.metric("Ventas Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("ROAS", "4.2x", "+0.5")
    m4.metric("Sincro Variantes", "Activa", "Colores/Talles")

    st.write("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA Estratégica:** He detectado productos con **Precio Tachado** que no tienen stock de variantes (Talle L, Color Azul). ¿Deseas que el sistema ajuste las ofertas automáticamente para evitar rebotes?")
        if st.button("🎯 Optimizar Variantes y Ofertas"):
            with st.status("Analizando catálogo...", expanded=True) as s:
                time.sleep(1)
                s.update(label="Sincronizando precios tachados...", state="running")
                time.sleep(1)
                s.update(label="Ajustando stock de variantes con ERP...", state="complete")
            st.balloons()
    with col_r:
        st.markdown("#### ⚡ Sincronización IA")
        st.caption("✅ Nombres y Enlaces")
        st.caption("✅ Stock por Variante")
        st.caption("✅ Lógica de Precios de Oferta")
        st.info("💡 **Insight:** El 40% de tus ventas provienen de variantes con descuento.")

with tab_ins:
    st.markdown("### 🧠 Soluciones con Visión de Mercado")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Gestión de Ofertas</h4><p>Nuestra IA utiliza el "precio anterior" para crear urgencia predictiva.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO (Search IA)</h4><p>Indexación de descripciones para ser la primera opción en chats de IA.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>Sincro de Variantes</h4><p>Control total de SKU por color y talle desde el ERP.</p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🧬 Simulación de Crecimiento")
    st.line_chart(pd.DataFrame(np.random.randint(100, 250, size=(15, 2)), columns=['Ventas con IA', 'Ventas Estándar']))



with tab_team:
    st.markdown("### 👥 Equipo UTEL")
    equipo = [("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"), ("Dalia R.", "Product Manager", "https://imgur.com/4O2BGL8.jpeg"), ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png")]
    cols = st.columns(3)
    for c, (n, cargo, img) in zip(cols, equipo):
        with c: st.markdown(f'<div class="team-card-large"><img src="{img}" style="width:180px;height:180px;border-radius:50%;object-fit:cover;border:6px solid #0056ff;margin-bottom:15px;"><br><strong>{n}</strong><br>{cargo}</div>', unsafe_allow_html=True)

st.caption("Impulsa IA | Hackathon 2026 | Desarrollado con técnicas avanzadas de integración Tiendanube")
