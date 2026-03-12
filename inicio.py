import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

# --- ESTADO DE LA SESIÓN (Lógica de Negocio Real) ---
if 'data_inventario' not in st.session_state:
    st.session_state.data_inventario = pd.DataFrame({
        "Producto": ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"],
        "Stock Actual": [5, 80, 25, 2],
        "Ventas_Dia": [4.2, 0.1, 1.5, 3.8],
        "Costo": [1200, 300, 150, 850]
    })

# --- ESTILOS CSS (Efectos Flowmerce Integrados) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp {{ background-color: #f4f7fb; font-family: 'Inter', sans-serif; }}
    
    .main-title {{
        background: linear-gradient(90deg, #2D3436, #0052D4, #4364F7);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important; font-weight: 800;
        animation: gradient-move 5s ease infinite;
    }}
    
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .card {{
        background: white; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #0052D4;
        transition: transform 0.3s ease; text-align: center;
    }}
    .card:hover {{ transform: translateY(-5px); border-top: 5px solid #4364F7; }}

    .metric-value {{ font-size: 2rem; font-weight: 800; color: #0052D4; }}

    .team-card-large {{
        text-align: center; padding: 15px; border-radius: 20px;
        background: white; border: 1px solid rgba(0, 82, 212, 0.1);
        box-shadow: 0px 10px 20px rgba(0,0,0,0.03);
        transition: all 0.4s ease;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR INTERACTIVO ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.markdown("### ⚡ Control de Datos API")
    if st.button("🔄 Sincronizar Tiendanube"):
        with st.spinner("Conectando con el inventario..."):
            time.sleep(1.5)
            # Modificación real de datos
            st.session_state.data_inventario["Stock Actual"] = np.random.randint(0, 100, 4)
            st.success("¡Inventario actualizado!")

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown("### Inteligencia de Capital: De inventario estancado a flujo de caja.")

# --- TABS FUNCIONALES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Monitor de Liquidez", "🤖 Estrategia IA", "🚀 El Pitch", "👥 Equipo"])

with tab1:
    # Cálculos dinámicos basados en el estado actual
    df = st.session_state.data_inventario
    atrapado = df[df["Stock Actual"] > 50].apply(lambda x: x["Stock Actual"] * x["Costo"], axis=1).sum()
    quiebre = len(df[df["Stock Actual"] < 5])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="card"><div style="color:#555;">Capital Atrapado</div><div class="metric-value">${atrapado:,} MXN</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><div style="color:#e53935;">Riesgo de Quiebre</div><div class="metric-value">{quiebre} SKUs</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><div style="color:#43a047;">Salud de Flujo</div><div class="metric-value">88%</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("#### ⚡ Simulador de Crisis Logística (Impacto en Caja)")
    retraso = st.slider("Días de retraso del proveedor:", 0, 30, 5)
    
    # Gráfico que reacciona al slider
    dias = pd.date_range(start='2026-03-12', periods=30)
    flujo_base = np.linspace(60000, 120000, 30) - (retraso * 2000)
    st.area_chart(pd.DataFrame({"Flujo de Caja Estimado": flujo_base}, index=dias))

with tab2:
    st.markdown("### 🤖 Motor de Decisiones Automáticas")
    
    # Tabla interactiva con lógica de decisión
    df_logic = st.session_state.data_inventario.copy()
    df_logic["Acción Sugerida"] = df_logic["Stock Actual"].apply(
        lambda x: "🚨 COMPRAR YA" if x < 10 else ("🔥 LIQUIDAR" if x > 60 else "✅ MANTENER")
    )
    st.dataframe(df_logic, use_container_width=True)
    
    if st.button("⚡ Ejecutar Estrategia Flowmerce"):
        st.balloons()
        st.success("Órdenes sincronizadas y campañas de liquidación activadas en Tiendanube.")

    st.divider()
    st.markdown("#### 🎤 Consulta Rápida (IA Voice)")
    audio = mic_recorder(start_prompt="Preguntar a Flowmerce", stop_prompt="Procesar", key='voice_flow')
    if audio:
        st.info("🤖 **Flowmerce IA:** Detecto exceso de stock en 'Gorra Urban'. Recomiendo cupón del 15% para liberar $4,500.")

with tab3:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.error("### 🚩 El Problema")
        st.write("Las tiendas quiebran por capital atrapado o falta de stock. La intuición no escala.")
    with col_p2:
        st.success("### 💡 La Solución")
        st.write("Flowmerce: IA que analiza velocidad de venta y reabastece automáticamente.")
    
    st.info("**Impacto Estratégico:** Reducción del 40% en inventario inmovilizado y +15% en ventas.")
    st.markdown("<h4 style='text-align: center; color: #0052D4;'>“No vendemos software. Vendemos decisiones que protegen tu capital.”</h4>", unsafe_allow_html=True)

with tab4:
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img_url}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #0052D4; margin-bottom: 10px;">
                    <div style="font-weight: 800; color: #1a1c2e; font-size: 0.85rem;">{nombre}</div>
                    <div style="color: #0052D4; font-size: 0.7rem; font-weight: 700;">{cargo}</div>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Flowmerce | Hackathon UTEL 2026 | Equipo 3 | TiendaNube")
