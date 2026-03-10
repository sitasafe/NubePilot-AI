import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Botón con degradado */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white; border-radius: 25px; border: none; padding: 12px 30px;
        font-weight: bold; width: 100%;
    }

    /* Título Moderno */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; margin-bottom: 0;
    }
    
    /* Estilo para tarjetas de equipo */
    .team-card {
        text-align: center;
        padding: 10px;
        border-radius: 15px;
        background: white;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .team-img { width: 40px !important; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.divider()
    st.markdown("### ⚙️ Configuración")
    with st.expander("🔑 API Key", expanded=False):
        st.code("shpat_live_942_growth_copilot_2026")
    st.success("Tienda: **Sitasafe Store**")
    st.info("💡 **Tip:** El análisis de sentimientos detectó que tus clientes aman el packaging.")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Estrategia inteligente para tu Tiendanube")

# --- NAVEGACIÓN POR PESTAÑAS (Limpieza Visual) ---
tab_dash, tab_insights, tab_team = st.tabs(["📊 Dashboard", "🧠 Insights AI", "👥 Equipo"])

with tab_dash:
    # Métricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m2.metric("Ventas Mes", "$12,450 MXN", "↑ 12%")
    m3.metric("Ventas Perdidas", "$1,500 MXN", "-200")

    st.divider()
    col_l, col_r = st.columns([2, 1])

    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **Sugerencia Automática:**")
            st.write("Detecté 12 carritos recuperables. El cupón **GROWTH10** tiene 88% de probabilidad de éxito.")
        
        if st.button("🎯 Aplicar Estrategia"):
            with st.status("Sincronizando..."): time.sleep(1)
            st.balloons()
            st.success("Estrategia activa en Tiendanube")

    with col_r:
        st.markdown("#### 💬 Consultar a la IA")
        q = st.text_input("", placeholder="¿Cómo mejorar ventas?")
        if st.button("Consultar"):
            st.caption("Respuesta IA: Optimiza stock en 'Cámaras WiFi'.")

with tab_insights:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🛒 Productos en Riesgo")
        st.table(pd.DataFrame({
            "Producto": ["Playera", "Gorra", "Tenis"],
            "Abandonos": [8, 3, 1],
            "Pérdida": ["$800", "$450", "$250"]
        }))
    with c2:
        st.markdown("#### 📈 Proyección de Impacto")
        st.line_chart(pd.DataFrame({"Ventas": [10, 20, 15, 40, 50, 65, 80]}))

with tab_team:
    st.markdown("### 👥 Nuestro Equipo - Grupo 3")
    st.write("Talento multidisciplinario detrás de AI Growth Copilot.")
    
    equipo = [
        ("Dalia Paola R.", "Capitana", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Willan Álvarez", "Lead Architect", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Montserrat G.", "Fotografía", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"),
        ("Cesar Augusto", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png"),
        ("Edwing Garcia", "Ventas", "https://cdn-icons-png.flaticon.com/512/9431/9431149.png"),
        ("Carlos Andrés", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png")
    ]
    
    # Grid de 4 columnas para que los iconos no se vean gigantes
    rows = [equipo[i:i + 4] for i in range(0, len(equipo), 4)]
    for row in rows:
        cols = st.columns(4)
        for i, (nombre, rol, icon) in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class="team-card">
                    <img src="{icon}" class="team-img"><br>
                    <strong>{nombre}</strong><br>
                    <small style='color:#666'>{rol}</small>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | Powered by Tiendanube | Hackathon UTEL 2026")
