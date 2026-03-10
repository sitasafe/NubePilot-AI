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
    
    /* Botón con degradado dinámico */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 18px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3);
    }

    /* Título con estilo moderno */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    
    /* Estilo para los nombres del equipo */
    .member-name { font-weight: bold; font-size: 14px; margin-bottom: -5px; }
    .member-skill { color: #6c757d; font-size: 12px; font-style: italic; }
    
    /* Tarjeta de Próximos Pasos */
    .next-steps {
        background-color: #eef2ff;
        padding: 15px;
        border-left: 5px solid #0056ff;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # --- LOGO DE TIENDANUBE (URL DIRECTA PARA EVITAR ERRORES) ---
    # Usamos la versión oficial de la nube para asegurar que cargue en Streamlit Cloud
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Conexión API", expanded=True):
        st.info("Estatus: Tiendanube Secure Link")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Tu estratega de crecimiento inteligente")
st.write("---")

# --- SECCIÓN: ESTADO ACTUAL DE LA TIENDA ---
st.markdown("### 📊 Estado Actual de la Tienda")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
with m_col2:
    st.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
with m_col3:
    st.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200")

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- MÓDULO DE IA GENERATIVA ---
    with st.chat_message("assistant
