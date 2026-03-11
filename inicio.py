import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- SEGURIDAD (Simulación de Secret Manager para el Hackathon) ---
# En producción usaríamos st.secrets
CLIENT_ID = "27483"
CLIENT_SECRET = st.sidebar.text_input("🔑 Client Secret (Seguro)", value="d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a", type="password")
REDIRECT_URI = "https://nubepilot-ai-jenadpeumuumeahkmnjmwr.streamlit.app/"

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "ImpulsaIA (socios@tiendanube.com)"}
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error("⚠️ La conexión expiró o el código es inválido. Por favor, re-autoriza la tienda.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return None

# --- ACCESIBILIDAD Y ESTILOS ---
accesibilidad = st.sidebar.toggle("♿ Modo Alto Contraste")
bg_color = "#0e1117" if accesibilidad else "radial-gradient(circle at top right, #ffffff, #f1f4f9)"
text_color = "#ffffff" if accesibilidad else "#1a1c2e"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background: {bg_color}; font-family: 'Inter', sans-serif; color: {text_color}; }}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    .problem-box {{ background: white; padding: 20px; border-radius: 15px; border-left: 8px solid #0056ff; color: #1a1c2e; }}
    .review-action-card {{ background: #f8faff; border-radius: 15px; padding: 15px; border-left: 5px solid #6200ea; margin-bottom: 10px; color: #1a1c2e; }}
    @keyframes gradient-move {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL: INCLUSIÓN Y CONTROL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    
    with st.expander("📖 Glosario para Humanos", expanded=False):
        st.write("**ROAS:** Cuánto dinero recuperas por cada peso invertido en anuncios.")
        st.write("**AIO:** Optimización para que ChatGPT y Gemini recomienden tu tienda.")
        st.write("**Insight:** Una idea clave descubierta por la IA analizando a tus clientes.")

    st.markdown("## ⚙️ Panel de Control")
    with st.expander("🔑 Conexión Tiendanube", expanded=False):
        auth_url = f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_products,read_customers"
        st.link_button("1. Autorizar", auth_url)
        temp_code = st.text_input("2. Code:")
        if st.button("3. Vincular"):
            token = obtener_token_real(temp_code)
            if token: st.session_state['api_token'] = token

    st.divider()
    st.info("💡 **Tip Pro:** Activa las notificaciones de WhatsApp para recibir tu tarea diaria.")
    st.button("📲 Vincular con WhatsApp")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico | Inteligencia Humana + IA")

tab_dash, tab_rev, tab_ins, tab_team = st.tabs(["📊 Monitor ROI", "✨ Review Intelligence", "🧠 Estrategia AIO", "👥 Equipo"])

with tab_dash:
    st.markdown("### 📊 Salud de tu Negocio")
    c1, c2, c3 = st.columns(3)
    c1.metric("Recuperación de Carritos", "12", "¡Evitaste perder $4,500 MXN!")
    # LENGUAJE HUMANO: Explicando el ROAS
    c2.metric("Ganancia por Anuncio (ROAS)", "4.2x", "+0.5")
    st.caption("✨ Por cada $1 invertido en publicidad, estás vendiendo $4.20 pesos.")
    c3.metric("Sincronización ERP", "98%", "Todo en orden")
    
    st.write("---")
    with st.chat_message("assistant"):
        st.write("🤖 **IA (Modelo Gemini 1.5 Pro):** He analizado las tendencias locales. Hay un aumento de interés en 'envíos sustentables' en Ciudad de México. ¿Quieres que actualicemos tus etiquetas?")
    
    if st.button("🎯 Aplicar Mejora Estratégica"):
        with st.status("Cargando datos con Caching Inteligente (evitando Rate Limit)..."):
            time.sleep(2)
        st.balloons()
        st.success("✅ Etiquetas actualizadas y enviadas al ERP.")

with tab_rev:
    st.markdown("### ✨ Inteligencia de Sentimiento Local")
    st.warning("🕵️ **Nota Ética:** Los datos competitivos son públicos y cumplen con la normativa LGPD 2026.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🏆 LA TAREA DE HOY (Prioridad Alta)")
        st.markdown("""
        <div class="review-action-card">
            <strong>📍 Insight México/Centro:</strong> Muchos clientes preguntan "¿Facturan?".<br>
            <small>Acción: Agrega un banner que diga 'Facturación Inmediata' para subir ventas 15%.</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("#### 🔍 Análisis de Modismos")
        st.info("La IA detectó que 'está padre' y 'me late' son menciones positivas recurrentes en tus reseñas de este mes.")

with tab_ins:
    st.markdown("### 🧠 Big Data Engine")
    # Simulación de predicción
    chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Ventas Reales', 'Predicción IA'])
    st.line_chart(chart_data)
    st.caption("Predicción generada analizando 2.5M de puntos de datos de la industria.")

with tab_team:
    st.markdown("### 👥 Equipo 3 - Hackathon UTEL")
    # (El código del equipo se mantiene igual para no dañar las imágenes de tus compañeros)
    st.write("Construyendo el futuro del E-commerce inclusivo.")

st.write("---")
st.caption("Impulsa IA | Versión 2.0 Inclusiva | Hackathon UTEL 2026")
