import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

# --- CREDENCIALES ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- LÓGICA DE DATOS SIMULADOS ---
def get_predictive_data():
    dias = pd.date_range(start='2026-03-12', periods=30)
    ventas = np.random.normal(5000, 1000, 30).cumsum()
    caja = ventas * 0.3 + 20000
    return pd.DataFrame({"Fecha": dias, "Ventas Estimadas": ventas, "Flujo de Caja": caja}).set_index("Fecha")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.markdown("### 🌐 Accesibilidad")
    idioma = st.selectbox("Idioma Interfaz", ["Español", "English", "Português", "Náhuatl", "Maya"])
    lectura_facil_on = st.toggle("Modo Lectura Fácil")
    contraste_alto = st.toggle("Modo Alto Contraste")
    
    st.divider()
    st.markdown("### 🔑 Conexión Tiendanube")
    if st.button("🔄 Sincronizar API"):
        with st.spinner("Conectando..."):
            time.sleep(1.5)
            st.success("Datos de Inventario Sincronizados")

# --- ESTILOS CSS (Efectos Visuales + Accesibilidad) ---
extra_styles = ""
if lectura_facil_on:
    extra_styles += "html, body, [class*='st-'] { font-size: 1.2rem !important; }"
if contraste_alto:
    extra_styles += ".stApp { background: #000 !important; color: #FFF !important; } .card { background: #111 !important; border: 1px solid #FFF !important; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp {{ background-color: #f4f7fb; font-family: 'Inter', sans-serif; }}
    
    .main-title {{
        background: linear-gradient(90deg, #0052D4, #4364F7, #6FB1FC, #0052D4);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800;
        animation: gradient-move 4s ease infinite;
    }}
    
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .card {{
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #4364F7;
        transition: transform 0.3s ease;
    }}
    .card:hover {{ transform: translateY(-5px); }}

    .team-card-large {{
        text-align: center; padding: 25px; border-radius: 30px;
        background: white; border: 1px solid rgba(0, 82, 212, 0.1);
        box-shadow: 0px 15px 30px rgba(0,0,0,0.05);
        transition: all 0.4s ease; height: 100%;
    }}
    .team-card-large:hover {{
        transform: translateY(-10px);
        border: 1px solid #4364F7;
        box-shadow: 0px 20px 40px rgba(0, 82, 212, 0.15);
    }}

    .metric-value {{ font-size: 2.2rem; font-weight: 800; color: #0052D4; }}
    
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 NubeFlow</h1>', unsafe_allow_html=True)
st.markdown("### **Optimización de Caja e Inventario Predictivo.**")

st.write("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Inteligencia de Caja", "🤖 Decisiones IA", "👥 Equipo"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    metrics = [
        ("💰 Capital Atrapado", "$42,800 MXN", "Dinero en stock sin movimiento", "#0052D4"),
        ("⚠️ Ventas en Riesgo", "$12,300 MXN", "Pérdida por Stockout inminente", "#e53935"),
        ("🛡️ Días de Liquidez", "45 Días", "Salud de flujo de caja", "#43a047")
    ]
    
    for i, (titulo, valor, cap, color) in enumerate(metrics):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="card">
                <div style="font-weight:700; color:#555;">{titulo}</div>
                <div class="metric-value" style="color:{color};">{valor}</div>
                <div style="font-size:0.8rem; color:#888;">{cap}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("#### 📈 Proyección Financiera (Próximos 30 días)")
    st.area_chart(get_predictive_data())

with tab2:
    st.markdown("### 🤖 Centro de Decisiones NubeFlow")
    c_dec1, c_dec2 = st.columns([1.5, 1])
    
    with c_dec1:
        st.markdown("#### 🛒 Sugerencias de Inventario")
        data_compra = {
            "Producto": ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"],
            "Estatus": ["Alta Rotación", "Stock Muerto", "Estable", "Crítico"],
            "Acción IA": ["COMPRAR 35 u.", "LIQUIDAR HOY", "MANTENER", "COMPRAR 15 u."],
            "Impacto Caja": ["-$12,000", "+$4,500", "$0", "-$3,200"]
        }
        st.table(pd.DataFrame(data_compra))
        if st.button("🚀 Aplicar Estrategia en Tiendanube"):
            st.balloons()
            st.success("Estrategia sincronizada: Cupones de liquidación creados y órdenes de compra enviadas.")

    with c_dec2:
        st.markdown("#### ⚡ Simulador de Riesgos")
        retraso = st.slider("Días de retraso del proveedor:", 0, 30, 5)
        if retraso > 10:
            st.error(f"ALERTA: Un retraso de {retraso} días agota tu caja en 2 semanas.")
        else:
            st.info("Escenario seguro. Tu liquidez soporta el retraso.")

        st.divider()
        st.markdown("#### 🎤 Consulta por Voz")
        audio = mic_recorder(start_prompt="Preguntar a NubeFlow", stop_prompt="Analizar", key='fin_rec')
        if audio:
            st.info("🤖 **IA Analizando:** '¿Qué producto liquidar?' -> *Respuesta: Gorra Urban Blue (+$4,500 flujo)*")

with tab3:
    st.markdown("### 👥 El Equipo detrás de NubeFlow")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, img_url) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 4px solid #4364F7; margin-bottom: 15px;">
                    <div style="font-weight: 800; color: #1a1c2e;">{nombre}</div>
                    <div style="color: #4364F7; font-size: 0.8rem; font-weight: 700;">{cargo}</div>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("NubeFlow IA | Equipo 3 | Hackathon UTEL 2026")
