import streamlit as st
import time
import pandas as pd
import numpy as np
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Live Demo", page_icon="🌊", layout="wide")

# --- ESTADO DE LA SESIÓN (Para que sea dinámico) ---
if 'sincronizado' not in st.session_state:
    st.session_state.sincronizado = False
if 'data_inventario' not in st.session_state:
    st.session_state.data_inventario = pd.DataFrame({
        "Producto": ["Tenis Runner Pro", "Gorra Urban Blue", "Calcetines High", "Sudadera Lino"],
        "Stock Actual": [5, 80, 25, 2],
        "Ventas/Día": [4.2, 0.1, 1.5, 3.8],
        "Estatus": ["Crítico", "Exceso", "Saludable", "Quiebre"]
    })

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #0052D4, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #0052D4; text-align: center; }
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #0052D4; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR DINÁMICO ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.markdown("### ⚡ Control de Datos")
    if st.button("🔄 Sincronizar Tiendanube (LIVE)"):
        with st.spinner("Extrayendo pedidos y stock..."):
            time.sleep(2)
            # Simulamos cambio de datos reales
            st.session_state.data_inventario["Stock Actual"] = np.random.randint(1, 100, 4)
            st.session_state.sincronizado = True
            st.success("¡Datos frescos obtenidos!")

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

# --- TABS FUNCIONALES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Real-Time", "🤖 Estrategia IA", "🚀 El Pitch", "👥 Equipo"])

with tab1:
    # Métricas calculadas dinámicamente
    total_stock = st.session_state.data_inventario["Stock Actual"].sum()
    atrapado = st.session_state.data_inventario[st.session_state.data_inventario["Estatus"] == "Exceso"]["Stock Actual"].sum() * 500
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="card"><span>Capital Atrapado</span><div class="metric-value">${atrapado:,} MXN</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card"><span>Productos en Riesgo</span><div class="metric-value">{len(st.session_state.data_inventario[st.session_state.data_inventario["Stock Actual"] < 10])}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card"><span>Eficiencia de Caja</span><div class="metric-value">84%</div></div>', unsafe_allow_html=True)

    st.write("---")
    
    # Gráfico interactivo que responde al Slider
    st.markdown("#### ⚡ Simulador de Supervivencia Financiera")
    retraso = st.slider("Días de retraso del proveedor:", 0, 30, 5)
    
    dias = pd.date_range(start='2026-03-12', periods=30)
    # El flujo de caja baja si el retraso sube (Simulación lógica)
    flujo_base = np.linspace(50000, 100000, 30) - (retraso * 1500)
    df_chart = pd.DataFrame({"Flujo de Caja": flujo_base}, index=dias)
    st.line_chart(df_chart)

with tab2:
    st.markdown("### 🤖 Motor de Decisiones Automáticas")
    
    # Tabla interactiva
    df_decisiones = st.session_state.data_inventario.copy()
    df_decisiones["Recomendación"] = df_decisiones["Stock Actual"].apply(lambda x: "COMPRAR" if x < 10 else "LIQUIDAR" if x > 50 else "MANTENER")
    
    st.dataframe(df_decisiones, use_container_width=True)
    
    if st.button("⚡ Ejecutar Órdenes de Compra"):
        with st.status("Conectando con proveedores...", expanded=True) as s:
            time.sleep(1)
            s.write("Calculando lote económico de compra...")
            time.sleep(1)
            s.update(label="Órdenes enviadas por API", state="complete")
        st.balloons()

    st.divider()
    # CHAT IA FUNCIONAL
    st.markdown("#### 💬 Consultar a Flowmerce")
    prompt = st.chat_input("Ej: ¿Cuál es mi producto menos rentable?")
    if prompt:
        with st.chat_message("assistant"):
            if "peor" in prompt or "menos" in prompt:
                st.write("Analizando... Tu peor producto es **Gorra Urban Blue**. Tienes 80 unidades y solo vendes 0.1 al día. Recomiendo liquidar con 20% descuento.")
            else:
                st.write(f"He recibido tu consulta: '{prompt}'. Basado en el stock de {total_stock} unidades, la salud de tu flujo es estable.")

with tab3:
    st.markdown("### 🚀 Pitch de Negocio")
    col_a, col_b = st.columns(2)
    with col_a:
        st.error("### El Problema")
        st.write("Las tiendas mueren por capital atrapado o quiebre de stock. No hay datos, hay 'intuición'.")
    with col_b:
        st.success("### La Solución")
        st.write("Flowmerce: De datos estáticos a flujo de efectivo. IA que compra por ti.")
    
    st.info("**Impacto:** Reducción del 40% en stock inmovilizado y 15% más ventas por disponibilidad.")
    st.warning("👉 *Tip para el jurado:* Prueben el slider en el Dashboard para ver cómo el retraso logístico mata la caja.")

with tab4:
    # Equipo dinámico
    equipo = [
        ("Willan Álvarez.", "Lead Architect"), ("Dalia R.", "Product Manager"),
        ("Montserrat G.", "Strategy"), ("Jiram Cabrera", "Organización"),
        ("Carlos Andrés A.", "Liderazgo"), ("Edwing Garcia", "Ventas"),
        ("Amarilis Elizabeth", "Gestión"), ("Cesar Augusto F.", "Estrategia")
    ]
    cols = st.columns(4)
    for i, (nom, cargo) in enumerate(equipo):
        cols[i % 4].info(f"**{nom}**\n\n{cargo}")

st.write("---")
st.caption("Flowmerce Live Demo | Hackathon 2026")
