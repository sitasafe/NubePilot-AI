import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (COLORES Y BOTONES) ---
st.markdown("""
    <style>
    /* Color de fondo y texto principal */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Personalización de Botones */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(0, 198, 255, 0.4);
    }

    /* Estilo para las tarjetas de métricas */
    [data-testid="stMetricValue"] {
        color: #0056ff;
    }

    /* Títulos con degradado */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Autenticación API", expanded=True):
        st.info("Conexión Segura con Tiendanube")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.text_input("Access Token de API", type="password", value="token_seguro_activado")
    st.text_input("ID de Tienda", value="2831942")
    
    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado a: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Tu estratega de crecimiento con IA Generativa")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- MÓDULO DE IA GENERATIVA ---
    with st.chat_message("assistant"):
        st.write("🤖 **Ejecutando algoritmos de crecimiento...**")
        placeholder = st.empty()
        
        mensaje_ia = """**Análisis del Copilot finalizado:** He detectado una ventana de oportunidad en **12 carritos abandonados**. 

Tras procesar los patrones de demanda y la disponibilidad actual en el inventario, el sistema ha diseñado la siguiente estrategia de conversión:

El cupón **GROWTH10** es la herramienta óptima para incentivar el cierre de estas ventas con una probabilidad de éxito del 88%. ¿Deseas aplicar esta acción ahora?"""
        
        full_response = ""
        for char in mensaje_ia:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
        placeholder.markdown(full_response)
    
    st.write("")
    # BOTÓN DINÁMICO CON ESTILO
    if st.button("🎯 Activar Estrategia de Recuperación"):
        with st.status("IA Generativa sincronizando con API...", expanded=True) as status:
            st.write("Interpretando patrones de compra...")
            time.sleep(1)
            st.write("Generando código de descuento dinámico...")
            time.sleep(1)
            status.update(label="¡Estrategia Implementada!", state="complete", expanded=False)
        st.balloons()
        st.success("### ✅ ¡CUPÓN 'GROWTH10' CREADO EXITOSAMENTE!")

    # --- CHAT INTERACTIVO ---
    st.write("---")
    st.markdown("### 💬 Asesor Inteligente")
    user_input = st.text_input("Hazle una pregunta a tu Copilot:")
    
    if user_input:
        with st.chat_message("assistant"):
            with st.spinner("IA procesando datos..."):
                time.sleep(1.5)
                st.write("Basado en el análisis de inventario de **Sitasafe**, recomiendo optimizar la descripción de la 'Cerradura Inteligente' para mejorar la conversión.")

    # --- SECCIÓN DE PRODUCTOS ---
    st.write("---")
    st.markdown("### 📦 Análisis de Productos (Top Abandonados)")
    chart_data = pd.DataFrame({
        "Productos": ["Cámara WiFi", "Sensor Pro", "Primeros Auxilios", "Cerradura Smart"],
        "Vistos": [120, 95, 80, 45],
        "Abandonados": [42, 28, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Productos"))

with col_right:
    # Tarjeta de métricas con estilo
    st.markdown("### 📊 Métricas de Impacto")
    m1, m2 = st.columns(2)
    m1.metric("Ventas Recup.", "$450.00", "+12%")
    m2.metric("Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### 🏷️ Inteligencia de Precios")
    st.info("Tu precio está **3% por debajo** de la competencia.")
    
    st.write("---")
    st.markdown("#### Tendencia")
    tendencia_data = np.random.randn(20, 1).cumsum()
    st.area_chart(tendencia_data)
    
    st.divider()
    st.markdown("### 👥 Equipo 3")
    
    equipo = [
        ("Dalia Paola R. Trejo", "Capitana", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Willan Álvarez Carmona", "Lead Architect", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Montserrat Garcia B.", "Diseño/Redacción", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera Ramos", "Organización", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png")
    ]
    
    for nombre, skill, img in equipo:
        c1, c2 = st.columns([1, 4])
        c1.image(img, width=35)
        c2.markdown(f"**{nombre}** \n\n <small>{skill}</small>", unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | IA Generativa | Hackathon UTEL 2026")
