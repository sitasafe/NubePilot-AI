import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (MANTENIDOS) ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; border-radius: 25px !important; border: none !important; 
        padding: 12px 30px !important; font-weight: bold !important; transition: all 0.3s ease !important; 
        width: 100% !important; font-size: 18px !important;
    }
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 800; margin-bottom: 0;
    }
    .team-card-large {
        text-align: center; padding: 25px; border-radius: 20px;
        background: white; box-shadow: 0px 10px 20px rgba(0,0,0,0.05); margin-bottom: 25px;
    }
    .problem-box {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 5px solid #0056ff; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .big-data-card {
        background: #0e1117; color: white; padding: 20px; border-radius: 15px; border-top: 4px solid #00c6ff;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    st.write("---")
    st.markdown("## ⚙️ Configuración")
    api_token = st.text_input("Access Token", type="password")
    id_tienda = st.text_input("ID de Tienda", value="2831942")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("Tu Copiloto Estratégico para Vender Más en TiendaNube")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Centro de Mando Estratégico", "🧠 Big Data & Predictive AI", "👥 Equipo"])

# --- TAB 1: CENTRO DE MANDO ---
with tab_dash:
    st.markdown("### 📈 Monitor de Rendimiento y Rentabilidad")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Fuga de Capital", "12", "-15%", delta_color="normal")
    m_col2.metric("Ingresos Brutos", "$12,450 MXN", "↑ 12%")
    m_col3.metric("ROI / ROAS", "4.2x", "+0.5")
    m_col4.metric("Precisión ERP", "98%", "Sincronizado")

    st.write("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        with st.chat_message("assistant"):
            st.write("🤖 **IA:** He analizado 1.2M de eventos de navegación. Sugiero redistribuir presupuesto de Ads a la categoría 'Moda Hombre' por tendencia alza.")
        if st.button("🎯 Ejecutar Optimización de Rentabilidad"):
            st.success("¡Estrategia aplicada con éxito!")
    with col_r:
        st.markdown("### 💬 Advisor Inteligente")
        st.text_input("Consulta:", placeholder="¿Cómo bajar mi CPA?")

# --- TAB 2: BIG DATA & PREDICTIVE AI (LO NUEVO) ---
with tab_ins:
    st.markdown("### 🧬 Motor de Análisis de Datos Masivos")
    
    # Simulación de Big Data Analytics
    col_data1, col_data2 = st.columns([1.5, 1])
    
    with col_data1:
        st.markdown("#### 📈 Predicción de Ventas (Prophet Model)")
        # Crear datos de tendencia predictiva
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) / [10, 20] + [1, 1],
            columns=['Ventas Reales', 'Predicción IA']
        )
        st.line_chart(chart_data)
        st.caption("La línea clara muestra la tendencia proyectada para los próximos 15 días basada en historial de 2 años.")

    with col_data2:
        st.markdown("#### 🎯 Segmentación de Audiencia (Clustering)")
        st.markdown("""
        <div class="big-data-card">
            <p><strong>Total de Perfiles Analizados:</strong> 45,280</p>
            <ul>
                <li>💎 <strong>VIPs:</strong> 12% (LTV Alto)</li>
                <li>🔄 <strong>Recurrentes:</strong> 35% (Potencial)</li>
                <li>⚠️ <strong>En Riesgo:</strong> 18% (Churn)</li>
            </ul>
            <small>Análisis basado en modelo RFM (Recency, Frequency, Monetary).</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📩 Lanzar Campaña de Retención Big Data"):
            st.toast("Enviando ofertas personalizadas a perfiles 'En Riesgo'...")

    st.write("---")
    
    # Problemáticas Críticas (Mantenido)
    st.markdown("### 🧠 Soluciones a Problemáticas")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="problem-box"><h4>📈 Ads Efficiency</h4><p>Análisis de Big Data para optimización de ROAS.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="problem-box"><h4>🌐 AIO / SEO</h4><p>Análisis de semántica para buscadores de IA.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="problem-box"><h4>🔌 ERP Connect</h4><p>Ingesta de datos masivos de inventario.</p></div>', unsafe_allow_html=True)

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Equipo 3")
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
                st.markdown(f'<div class="team-card-large"><img src="{img_url}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 6px solid #0056ff; margin-bottom: 15px;"><br><strong>{nombre}</strong><br>{cargo}</div>', unsafe_allow_html=True)

st.caption("Impulsa IA | Equipo 3 | Hackathon UTEL 2026")
