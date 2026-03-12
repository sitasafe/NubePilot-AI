import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

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
    if st.button("🔄 Sincronizar Flowmerce"):
        with st.spinner("Vinculando con Tiendanube..."):
            time.sleep(1.5)
            st.success("Inventario Sincronizado")

# --- ESTILOS CSS (Identidad Flowmerce) ---
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
        background: linear-gradient(90deg, #2D3436, #0052D4, #4364F7);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800;
        animation: gradient-move 5s ease infinite;
    }}
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .card {{
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #0052D4;
        transition: transform 0.3s ease;
    }}
    .card:hover {{ transform: translateY(-5px); border-top: 5px solid #4364F7; }}
    .team-card-large {{
        text-align: center; padding: 20px; border-radius: 30px;
        background: white; border: 1px solid rgba(0, 82, 212, 0.1);
        box-shadow: 0px 10px 20px rgba(0,0,0,0.03);
        transition: all 0.4s ease; height: 100%;
    }}
    .metric-value {{ font-size: 2.2rem; font-weight: 800; color: #0052D4; }}
    .impact-box {{
        background: #eef2f7; padding: 20px; border-radius: 15px; border-left: 5px solid #0052D4; margin-bottom: 10px;
    }}
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown("### **Inteligencia de Capital:** Transformando inventario en flujo de efectivo.")

st.write("---")

# --- TABS ---
tab_pitch, tab_dash, tab_strat, tab_team = st.tabs(["🚀 Pitch & Impacto", "📊 Monitor de Liquidez", "🤖 Estrategia Predictiva", "👥 Equipo"])

with tab_pitch:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### 🚩 El Problema")
        st.info("Las tiendas no quiebran por falta de ventas... quiebran por **mala gestión de inventario**.")
        st.markdown("""
        - **Quiebre de stock:** Ventas perdidas que se van a la competencia.
        - **Exceso de inventario:** Capital inmovilizado "durmiendo" en estanterías.
        - **Merma y Obsolescencia:** Productos que pierden valor con el tiempo.
        """)
        st.markdown("### 💡 Nuestra Solución")
        st.success("**Flowmerce** transforma datos en decisiones automáticas de compra analizando velocidad de venta, historial y tiempos de entrega.")
    
    with col_p2:
        st.markdown("### 📈 Impacto Estimado")
        st.markdown('<div class="impact-box"><b>Ventas:</b> Incremento del 5% - 15%</div>', unsafe_allow_html=True)
        st.markdown('<div class="impact-box"><b>Stockouts:</b> Reducción del 30% - 50%</div>', unsafe_allow_html=True)
        st.markdown('<div class="impact-box"><b>Excedente:</b> Reducción del 20% - 40%</div>', unsafe_allow_html=True)
        st.markdown('<div class="impact-box"><b>Costos Logísticos:</b> Ahorro del 10% - 20%</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("<h4 style='text-align: center; color: #0052D4;'>“No vendemos software de inventario. Vendemos decisiones inteligentes que protegen el capital de las tiendas.”</h4>", unsafe_allow_html=True)

with tab_dash:
    col1, col2, col3 = st.columns(3)
    metrics = [
        ("💰 Capital Atrapado", "$42,800 MXN", "Stock sin rotación > 60 días", "#0052D4"),
        ("⚠️ Ventas Perdidas Proyectadas", "$12,300 MXN", "Impacto por falta de stock", "#e53935"),
        ("🛡️ Índice de Supervivencia", "45 Días", "Respaldo de caja actual", "#43a047")
    ]
    for i, (titulo, valor, cap, color) in enumerate(metrics):
        with [col1, col2, col3][i]:
            st.markdown(f'<div class="card"><div style="font-weight:700; color:#555;">{titulo}</div><div class="metric-value" style="color:{color};">{valor}</div><div style="font-size:0.8rem; color:#888;">{cap}</div></div>', unsafe_allow_html=True)
    st.write("---")
    st.markdown("#### 📈 Proyección de Flujo vs. Ventas (Próximos 30 días)")
    st.area_chart(get_predictive_data())

with tab_strat:
    st.markdown("### 🤖 Motor de Decisiones IA")
    c_dec1, c_dec2 = st.columns([1.5, 1])
    with c_dec1:
        st.markdown("#### 🛒 Sugerencias de Reabastecimiento Inteligente")
        data_compra = {
            "Producto": ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"],
            "Análisis IA": ["Alta Demanda", "Exceso de Stock", "Saludable", "Quiebre Inminente"],
            "Acción Sugerida": ["COMPRAR 35 u.", "GENERAR CUPÓN", "NO COMPRAR", "COMPRAR 15 u."],
            "Impacto Neto": ["-$12,000", "+$4,500", "$0", "-$3,200"]
        }
        st.table(pd.DataFrame(data_compra))
        if st.button("⚡ Ejecutar Estrategia Flowmerce"):
            st.balloons()
            st.success("Estrategia sincronizada con Tiendanube.")
    with c_dec2:
        st.markdown("#### ⚡ Simulador de Crisis Logística")
        retraso = st.slider("Días de retraso:", 0, 30, 5)
        if retraso > 10: st.error(f"¡Atención! Retraso crítico para tu reserva operativa.")
        else: st.info("Tu flujo de caja es resistente.")
        st.divider()
        st.markdown("#### 🎤 Consulta Rápida")
        audio = mic_recorder(start_prompt="Preguntar a Flowmerce", stop_prompt="Procesar", key='voice_flow')
        if audio: st.info("🤖 **Flowmerce IA:** Analizando... Te recomiendo liquidar 'Gorra Urban Blue'.")

with tab_team:
    st.markdown("### 👥 Nuestro Equipo")
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
                st.markdown(f'<div class="team-card-large"><img src="{img_url}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #0052D4; margin-bottom: 10px;"><div style="font-weight: 800; color: #1a1c2e; font-size: 0.9rem;">{nombre}</div><div style="color: #0052D4; font-size: 0.75rem; font-weight: 700;">{cargo}</div></div>', unsafe_allow_html=True)

st.write("---")
st.caption("Flowmerce | Hackathon UTEL 2026 | Equipo 3 | TiendaNube")
