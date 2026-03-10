import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Equipo 3", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white; border-radius: 25px; border: none;
        padding: 12px 30px; font-weight: bold; width: 100%;
    }
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800;
    }
    .member-card {
        background-color: #f1f3f5;
        padding: 10px; border-radius: 10px; margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # Logo de Tiendanube para validación de ecosistema
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Tiendanube_logo.svg/1200px-Tiendanube_logo.svg.png", width=150)
    st.write("---")
    st.markdown("### ⚙️ Conectividad")
    with st.expander("API Status", expanded=False):
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Token Activo ✅")
    st.divider()
    st.info("📍 Tienda: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("El cerebro inteligente para tu tienda online")

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- MÓDULO IA ---
    with st.chat_message("assistant"):
        st.write("🤖 **Procesando datos de Sitasafe...**")
        placeholder = st.empty()
        mensaje = """**Análisis finalizado:** He detectado **12 carritos abandonados**. 
        
Basado en tu stock y demanda, el cupón **GROWTH10** recuperará el 88% de estas ventas. ¿Lo activamos?"""
        full_res = ""
        for c in mensaje:
            full_res += c
            placeholder.markdown(full_res + "▌")
            time.sleep(0.005)
        placeholder.markdown(full_res)
    
    if st.button("🎯 Ejecutar Estrategia de Recuperación"):
        with st.status("Sincronizando con Tiendanube...", expanded=True):
            time.sleep(1)
            st.write("Cupón GROWTH10 creado en la plataforma.")
        st.balloons()
        st.success("¡Estrategia en marcha! Los clientes recibirán su notificación ahora.")

    # --- CHAT INTERACTIVO ---
    st.write("---")
    st.markdown("### 💬 Consulta a tu Asesor")
    pregunta = st.text_input("Hazle una pregunta a la IA (Ej: ¿Qué producto promocionar?):")
    if pregunta:
        with st.chat_message("assistant"):
            st.write("📊 Analizando tendencias... Recomiendo impulsar el **Kit de Primeros Auxilios**, la demanda ha subido un 15% esta semana.")

    # --- GRÁFICO ---
    st.write("---")
    st.markdown("### 📦 Productos más Abandonados")
    chart_data = pd.DataFrame({
        "Productos": ["Cámara WiFi", "Sensor Pro", "Kit Médico", "Cerradura Smart"],
        "Abandonados": [42, 28, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Productos"))

with col_right:
    st.markdown("### 📈 Impacto Real")
    c1, c2 = st.columns(2)
    c1.metric("Ventas Recup.", "$450.00", "+12%")
    c2.metric("Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### 🏷️ Pricing Intelligence")
    st.warning("Tu precio está 3% bajo la competencia. Podrías subirlo un 1% sin perder ventas.")
    
    st.write("---")
    st.markdown("#### 👥 Equipo 3")
    equipo = [
        ("Dalia Paola R. Trejo", "Capitana", "👩‍💼"),
        ("Willan Álvarez Carmona", "Lead Architect", "👨‍💻"),
        ("Montserrat Garcia B.", "Diseño", "🎨"),
        ("Jiram Cabrera Ramos", "Organización", "🤝"),
        ("Cesar Augusto F. Delgado", "Estrategia", "📊"),
        ("Edwing Garcia Juarez", "Ventas", "📢"),
        ("Carlos Andrés Almeida R.", "Liderazgo", "🚀"),
        ("Amarilis Elizabeth Vera G.", "Análisis", "🔍")
    ]
    for n, s, i in equipo:
        st.markdown(f"{i} **{n}** - <small>{s}</small>", unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | Hackathon UTEL 2026 - Presentación Final")
