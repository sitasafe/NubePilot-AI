import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubeFlow IA - Hackathon", page_icon="🌊", layout="wide")

# --- CREDENCIALES (Se mantienen igual) ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- DICCIONARIO DE IDIOMAS (ACTUALIZADO A NUBEFLOW) ---
textos = {
    "Español": {
        "sub": "De Excel a 5 minutos: Automatiza tu caja e inventario",
        "tab1": "📈 Flujo de Caja & Stock",
        "tab_ojo": "👁️ Escáner de Facturas (Ojo Nube)",
        "met1": "Capital Atrapado", "met2": "Días de Inventario"
    },
    "English": {
        "sub": "From Excel to 5 minutes: Automate your cash flow & inventory",
        "tab1": "📈 Cash Flow & Stock",
        "tab_ojo": "👁️ Invoice Scanner (Nube Eye)",
        "met1": "Stuck Capital", "met2": "Inventory Days"
    }
}

# --- ESTILOS NUBEFLOW (Océano/Confianza) ---
st.markdown(f"""
<style>
    .main-title {{
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800;
    }}
    .stMetric {{ background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
    .cash-warning {{ background-color: #fff3f3; padding: 20px; border-radius: 15px; border-left: 8px solid #ff4b4b; }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True) # Logo de equipo
    idioma = st.selectbox("Idioma", ["Español", "English"])
    st.divider()
    st.markdown("### 🌊 NubeFlow Status")
    st.success("Conectado a TiendaNube ✅")
    st.info("Sincronizado con Excel/ERP")

t_act = textos[idioma]

# --- CABECERA ---
st.markdown('<h1 class="main-title">🌊 NubeFlow IA</h1>', unsafe_allow_html=True)
st.subheader(t_act["sub"])
st.write("> *'Las tiendas no quiebran por falta de ventas, quiebran por falta de caja.'*")

st.divider()

# --- TABS ---
tab_flow, tab_scanner, tab_team = st.tabs([t_act["tab1"], t_act["tab_ojo"], "👥 Equipo"])

with tab_flow:
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric(t_act["met1"], "$45,200 MXN", delta="-15% (Dinero liberado)", delta_color="normal")
    col_m2.metric(t_act["met2"], "18 días", delta="Saludable")
    col_m3.metric("Ventas Proyectadas", "$120,000", "↑ 8% vs mes anterior")

    st.write("---")
    
    col_chart, col_insight = st.columns([2, 1])
    
    with col_chart:
        st.markdown("#### 📊 Proyección de Caja vs. Compras")
        chart_data = pd.DataFrame(
            np.random.randn(20, 2),
            columns=['Ventas Esperadas', 'Nivel de Stock Óptimo']
        )
        st.area_chart(chart_data)

    with col_insight:
        st.markdown('<div class="cash-warning">', unsafe_allow_html=True)
        st.markdown("#### ⚠️ Alerta de Liquidez")
        st.write("Tienes $15,000 MXN 'enterrados' en productos de baja rotación (Categoría: Accesorios).")
        if st.button("🔄 Liberar Capital"):
            with st.status("Creando campaña de liquidación en Tiendanube..."):
                time.sleep(2)
            st.success("Campaña de 20% descuento creada para liberar caja.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_scanner:
    st.markdown("### 👁️ Digitalización de Insumos (Ojo Nube)")
    st.write("Toma una foto a la factura de tu proveedor para actualizar NubeFlow sin usar Excel.")
    
    c_cam, c_data = st.columns(2)
    with c_cam:
        foto = st.camera_input("Escanear factura/nota")
    
    with c_data:
        if foto:
            with st.spinner("IA procesando costos y cantidades..."):
                time.sleep(2)
                st.info("📦 **Detección IA:** Se detectaron 20 unidades de 'Camisa Lino' con costo de $300. El impacto en tu flujo de caja será de -$6,000 el próximo lunes.")
                st.button("Confirmar y subir a Tiendanube")
        else:
            st.warning("Sube una foto para ver la magia de la IA.")

with tab_team:
    st.markdown("### 👥 Equipo NubeFlow")
    # (Aquí va tu lista de equipo igual que antes)
    st.write("Willan, Dalia, Montserrat, Jiram, Carlos, Edwing, Amarilis, Cesar.")

st.write("---")
st.caption("NubeFlow | Equipo 3 | Hackathon UTEL 2026")
