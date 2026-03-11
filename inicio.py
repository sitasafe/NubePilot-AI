import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- FUNCIONES DE CONEXIÓN API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    # Lógica de conexión (simplificada para que no falle el renderizado)
    return "token_demo_123" if code else None

# --- ESTILOS CSS ULTRA DINÁMICOS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    /* Fondo con gradiente animado */
    .stApp { 
        background: linear-gradient(-45deg, #ffffff, #f1f4f9, #e8efff, #ffffff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* Botón interactivo con efecto de escala */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 50px !important; 
        border: none !important; 
        padding: 18px 45px !important;
        font-weight: 800 !important; 
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
        width: 100% !important; 
        box-shadow: 0px 10px 25px rgba(0, 86, 255, 0.4) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) translateY(-5px) !important;
        box-shadow: 0px 15px 35px rgba(0, 86, 255, 0.6) !important;
    }

    /* Título con efecto Neón */
    .main-title {
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 5rem !important; 
        font-weight: 800; 
        animation: gradient-move 4s ease infinite;
        text-align: center;
    }

    /* Tarjetas que flotan al pasar el mouse */
    .problem-box, .team-card-large, .review-action-card {
        transition: all 0.4s ease !important;
        cursor: pointer;
    }
    .problem-box:hover, .review-action-card:hover {
        transform: translateY(-10px);
        box-shadow: 0px 15px 30px rgba(0,0,0,0.1) !important;
        border-color: #0056ff !important;
    }

    /* Animación para las fotos del equipo */
    .team-img {
        transition: all 0.5s ease;
        filter: grayscale(20%);
    }
    .team-img:hover {
        filter: grayscale(0%);
        transform: rotate(5deg) scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.markdown("## ⚙️ Panel de Control")
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP", "Manual"])
    
    with st.expander("🔑 Conexión Real Tiendanube", expanded=True):
        st.info("Paso 1: Autoriza la App")
        st.link_button("🚀 Autorizar en Tiendanube", "https://www.tiendanube.com/apps/authorize?client_id=27483")
        temp_code = st.text_input("Paso 2: Código de Retorno")
        if st.button("Vincular Ahora"):
            with st.spinner('Sincronizando inventario...'):
                time.sleep(2)
            st.success("¡Tienda Vinculada!")

# --- HEADER PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #444;'>Tu Copiloto Estratégico para Vender Más</h3>", unsafe_allow_html=True)
st.write("---")

# TABS DINÁMICOS
tab_dash, tab_rev, tab_ins, tab_team = st.tabs(["📊 Dashboard ROI", "✨ Review AI", "🧠 Estrategia AIO", "👥 Equipo"])

with tab_dash:
    st.markdown("### 📈 Estado de tu Tienda")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m2.metric("Ventas Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("ROAS Anuncios", "4.2x", "+0.5")
    m4.metric("Precisión ERP", "98%", "✓")
    
    st.write("---")
    c_l, c_r = st.columns([2, 1])
    with c_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA Impulsa:** 'Detecté que tus clientes buscan 'impermeables' los jueves. ¿Quieres que ajuste tu publicidad automáticamente?'")
        if st.button("🎯 EJECUTAR OPTIMIZACIÓN EN VIVO"):
            st.toast("Optimizando campañas...", icon="⚡")
            time.sleep(1)
            st.balloons()
            st.success("¡Publicidad optimizada para el clima de hoy!")
    with c_r:
        st.info("💡 **Tip Inteligente:** Tu producto estrella tiene un ROAS de 5.1x. ¡Inyecta presupuesto!")

with tab_rev:
    st.markdown("### ✨ Review Intelligence")
    st.markdown("<p style='color: #666;'>Analizamos miles de comentarios para darte tareas simples.</p>", unsafe_allow_html=True)
    
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("""
        <div class="review-action-card" style="border-left: 8px solid #ff4b4b;">
            <h4 style="color: #ff4b4b;">🔴 ACCIÓN URGENTE</h4>
            <p>Clientes reportan dificultad de armado en el modelo "Pro".</p>
            <strong>Solución:</strong> Subir video tutorial a la ficha de producto.
        </div>
        """, unsafe_allow_html=True)
    with c_b:
        st.markdown("""
        <div class="review-action-card" style="border-left: 8px solid #00c6ff;">
            <h4 style="color: #00c6ff;">💡 OPORTUNIDAD</h4>
            <p>Tus competidores fallan en la cremallera. La tuya es top.</p>
            <strong>Solución:</strong> Resalta "Cremallera Reforzada" en tu anuncio.
        </div>
        """, unsafe_allow_html=True)

with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="problem-box"><h4>Ads 2.0</h4><p>Ajuste en tiempo real según el clima y tendencias.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="problem-box"><h4>AIO (AI Optimization)</h4><p>Aparece primero cuando alguien pregunta a ChatGPT.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="problem-box"><h4>ERP Sync</h4><p>Adiós al quiebre de stock. Holded y SAP al 100%.</p></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### 🧬 Análisis de Tendencias")
    df_chart = pd.DataFrame({
        "Ventas": np.random.randint(100, 200, 15),
        "Predicción IA": np.random.randint(150, 250, 15)
    })
    st.line_chart(df_chart)

with tab_team:
    st.markdown("### 👥 El Cerebro detrás de Impulsa")
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" class="team-img" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff; margin-bottom: 15px;">
                    <br><strong>{nombre}</strong><br>
                    <span style="color: #0056ff; font-size: 0.9em;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("🚀 Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
