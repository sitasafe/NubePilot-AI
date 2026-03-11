import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    
    /* Botón con degradado dinámico */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 25px !important; 
        border: none !important; 
        padding: 12px 30px !important;
        font-weight: bold !important; 
        transition: all 0.3s ease !important; 
        width: 100% !important; 
        font-size: 18px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
    }

    /* Título con estilo moderno */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; 
        font-weight: 800; 
        margin-bottom: 0;
    }
    
    /* Tarjetas de Equipo */
    .team-card-large {
        text-align: center; 
        padding: 25px; 
        border-radius: 20px;
        background: white; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05); 
        margin-bottom: 25px;
    }

    /* Estilo para las métricas de Ads/SEO */
    .problem-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0056ff;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Generador de Access Token", expanded=True):
        temp_code = st.text_input("Pega el 'Code' de Partners aquí")
        if st.button("Generar Token"):
            if temp_code:
                st.success("¡Token Creado!")
                st.code("shpat_6f8b9e2d4c1a5b0z9y8x7w6v5u4t3s2r1")
                st.info("⬆️ COPIA este código y pégalo abajo")
            else:
                st.warning("Escribe el código primero.")

    st.divider()
    
    api_token = st.text_input("Access Token de API", type="password", help="Pega el token generado arriba")
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token:
        st.success("Estado: Conectado ✅")
    else:
        st.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Dashboard General", "🧠 Insights y Optimización", "👥 Equipo"])

# --- TAB 1: DASHBOARD GENERAL (Incluyendo problemáticas Ads/SEO) ---
with tab_dash:
    st.markdown("### 📊 Salud de la Tienda y Rendimiento")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS Promedio", "4.2x", "+0.5")
    m_col4.metric("SEO Score", "82/100", "↑ 5%")

    st.write("---")
    
    col_left, col_right = st.columns([2, 1])

    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA de Impulsa:** Hola, detecté que tu **ROAS** en Meta Ads bajó un 10% hoy. ¿Quieres que optimice el presupuesto hacia los productos con mejor margen?")
        
        if st.button("🎯 Activar Estrategia de Recuperación"):
            with st.status("Conectando con la API de Tiendanube y Meta Ads...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Analizando eficiencia en Ads...", state="running")
                time.sleep(1)
                status.update(label="Sincronizando con ERP para verificar stock...", state="running")
                time.sleep(1)
                status.update(label="¡Optimización Desplegada!", state="complete", expanded=False)
            
            st.balloons()
            st.success("### 🚀 Estrategia aplicada: Presupuesto optimizado y Cupón SITASAFE10 activado.")

    with col_right:
        st.markdown("### 💬 Asesor Inteligente")
        u_input = st.text_input("Consulta a la IA (Ads, SEO, Stock):", placeholder="¿Por qué bajó mi ROAS?")
        if st.button("Enviar"):
            st.info(f"📊 **IA:** El ROAS bajó porque el producto 'Playera Algodón' se quedó sin stock en el ERP. He pausado ese anuncio automáticamente.")

# --- TAB 2: INSIGHTS AVANZADOS (Alineado a las necesidades del Hackathon) ---
with tab_ins:
    st.markdown("### 🧠 Solución a Problemáticas Críticas")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="problem-box">
            <h4>📈 Eficiencia en Ads</h4>
            <p>Monitoreo de ROAS en tiempo real y ajuste de pujas automático.</p>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="problem-box">
            <h4>🌐 SEO / AIO</h4>
            <p>Generación de descripciones optimizadas para buscadores y asistentes de IA.</p>
            </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="problem-box">
            <h4>🔌 ERP Connect</h4>
            <p>Sincronización total de inventario para evitar ventas sin stock.</p>
            </div>""", unsafe_allow_html=True)

    st.write("---")
    
    col_ins1, col_ins2 = st.columns([1, 1])
    with col_ins1:
        st.markdown("#### 🚩 Hoja de Ruta SEO")
        st.error("🚨 **ALERTA:** 5 productos no tienen Meta-descripción.")
        st.warning("⚠️ **OPORTUNIDAD:** Tu competencia está posicionando mejor en 'Ropa Sustentable'.")
        st.info("💡 **DATO:** Optimizar imágenes reduciría el rebote en un 15%.")

    with col_ins2:
        st.markdown("#### 📊 Comparativa de Sentimiento")
        data_sentimiento = pd.DataFrame({
            "Categoría": ["Calidad", "Envío", "Atención", "Precio"],
            "Tu Tienda": [85, 70, 90, 65],
            "Competencia": [80, 85, 75, 70]
        }).set_index("Categoría")
        st.bar_chart(data_sentimiento)

# --- TAB 3: EQUIPO (FOTOS GRANDES) ---
with tab_team:
    st.markdown("### 👥 Equipo 3 - Desarrollo y Estrategia")
    
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="
                        width: 200px; 
                        height: 200px; 
                        border-radius: 50%; 
                        object-fit: cover; 
                        border: 6px solid #0056ff; 
                        margin-bottom: 15px;
                        box-shadow: 0px 8px 15px rgba(0,0,0,0.1);
                    ">
                    <br><strong style="font-size: 1.4rem;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 600;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")

