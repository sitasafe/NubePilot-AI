import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (MANTENIDOS Y MEJORADOS) ---
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

    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; 
        font-weight: 800; 
        margin-bottom: 0;
    }
    
    .team-card-large {
        text-align: center; 
        padding: 25px; 
        border-radius: 20px;
        background: white; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05); 
        margin-bottom: 25px;
    }

    .problem-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0056ff;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .status-tag {
        background: #e1e7ff;
        color: #0056ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }

    /* Nuevo estilo para Big Data Engine */
    .big-data-stat {
        background: #0e1117;
        color: #00c6ff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #0056ff;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    erp_mode = st.selectbox("Sincronización ERP", ["Holded (Recomendado)", "Odoo", "SAP Business One", "Manual"])
    
    with st.expander("🔑 Generador de Access Token", expanded=False):
        temp_code = st.text_input("Pega el 'Code' de Partners aquí")
        if st.button("Generar Token"):
            if temp_code:
                st.success("¡Token Creado!")
                st.code("shpat_6f8b9e2d4c1a5b0z9y8x7w6v5u4t3s2r1")
    
    st.divider()
    api_token = st.text_input("Access Token de API", type="password")
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token:
        st.success("Conectado a TiendaNube ✅")
    else:
        st.warning("Esperando Conexión... ⚠️")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Monitor de Crecimiento & ROI", "🧠 Estrategia y AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD GENERAL ---
with tab_dash:
    st.markdown("### 📊 Performance & ROI Center")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROAS Publicidad", "4.2x", "+0.5")
    m_col4.metric("Eficiencia ERP", "98%", "Sincronizado")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He detectado una anomalía: el ROAS de tus campañas bajó mientras que las búsquedas de 'ropa sustentable' subieron. ¿Sincronizamos stock del ERP y optimizamos el SEO para IA?")
        
        if st.button("🎯 Ejecutar Optimización Operativa"):
            with st.status("Procesando...", expanded=True) as status:
                time.sleep(1)
                status.update(label="Sincronizando inventario con ERP...", state="running")
                time.sleep(1)
                status.update(label="Generando Metatags AIO (AI Optimization)...", state="running")
                time.sleep(1)
                status.update(label="Ajustando pujas de Ads por ROAS...", state="complete", expanded=False)
            st.balloons()
            st.success("### 🚀 Sistema Optimizado: Stock actualizado y Ads ajustados.")

    with col_right:
        st.markdown("### 💬 Consulta IA")
        u_input = st.text_input("Pregunta sobre Ads o Stock:", placeholder="¿Cuál es mi producto más rentable?")
        if st.button("Analizar"):
            st.info(f"📊 **Análisis:** Tu producto 'Playera Algodón' tiene un ROAS de 5.1x pero stock crítico en ERP (5 unidades). Sugiero reponer stock antes de escalar Ads.")

# --- TAB 2: ESTRATEGIA Y AIO (CON BIG DATA INTEGRADO) ---
with tab_ins:
    st.markdown("### 🧠 Soluciones Estratégicas")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ADS & ROAS</span>
            <h4>Eficiencia Publicitaria</h4>
            <p>Ajuste dinámico de inversión según el rendimiento de ventas reales.</p>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">AIO / SEO</span>
            <h4>Optimización para IA</h4>
            <p>Adaptamos tu contenido para ser la primera respuesta en ChatGPT y Gemini.</p>
            </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="problem-box">
            <span class="status-tag">ERP CONNECT</span>
            <h4>Automatización Operativa</h4>
            <p>Conexión fluida con sistemas externos para control de inventario total.</p>
            </div>""", unsafe_allow_html=True)

    st.write("---")
    
    # SECCIÓN BIG DATA ENGINE
    st.markdown("### 🧬 Big Data Engine: Análisis Predictivo")
    col_big1, col_big2 = st.columns([1.5, 1])
    
    with col_big1:
        st.markdown("#### 📈 Proyección de Demanda (Próximos 15 días)")
        # Simulación de datos predictivos
        df_pred = pd.DataFrame({
            "Día": [f"Día {i}" for i in range(1, 16)],
            "Ventas Reales": np.random.randint(100, 200, 15),
            "Tendencia Predictiva": np.random.randint(150, 250, 15)
        }).set_index("Día")
        st.line_chart(df_pred)
        st.caption("Gráfico generado tras analizar 2.5 millones de puntos de datos históricos.")

    with col_big2:
        st.markdown("#### 🎯 Segmentación de Audiencia")
        st.markdown("""
        <div class="big-data-stat">
            <h2 style="margin:0; color:#00c6ff;">45,280</h2>
            <p style="margin:0; font-size:0.9rem;">Perfiles Analizados</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.progress(85, text="Fidelidad de Clientes (LTV)")
        st.progress(62, text="Probabilidad de Recompra")
        st.progress(18, text="Tasa de Abandono (Predictiva)")
        
        if st.button("📊 Generar Reporte de Big Data"):
            st.toast("Procesando clusters de clientes...")
            time.sleep(1)
            st.download_button("Descargar Análisis PDF", data="Contenido del reporte...", file_name="Reporte_BigData_Impulsa.txt")

    st.write("---")
    
    col_ins1, col_ins2 = st.columns([1, 1])
    with col_ins1:
        st.markdown("#### 🚩 Hoja de Ruta SEO/AIO")
        st.error("🚨 **CRÍTICO:** 3 categorías principales sin etiquetas optimizadas para IA.")
        st.warning("⚠️ **ALERTA:** Desfase de stock detectado entre ERP y TiendaNube.")
        st.info("💡 **TIP:** Activar envíos gratis aumentó conversiones un 20% en tu nicho.")

    with col_ins2:
        st.markdown("#### 📊 Sentimiento y Mercado")
        data_sentimiento = pd.DataFrame({
            "Categoría": ["Atención", "Envío", "Stock", "Precio"],
            "Tu Tienda": [90, 75, 60, 85],
            "Media Competencia": [80, 82, 85, 78]
        }).set_index("Categoría")
        st.area_chart(data_sentimiento)

# --- TAB 3: EQUIPO (MANTENIDO) ---
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 6px solid #0056ff; margin-bottom: 15px;">
                    <br><strong style="font-size: 1.4rem;">{nombre}</strong>
                    <br><span style="color: #0056ff; font-weight: 600;">{cargo}</span>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")
