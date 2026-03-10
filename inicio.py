import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Autenticación API", expanded=True):
        st.info("Conexión Segura con Tiendanube")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.write("---")
    st.text_input("Access Token de API", type="password", value="token_seguro_activado")
    st.text_input("ID de Tienda", value="2831942")
    
    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado a: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown("# 🚀 AI Growth Copilot")
st.subheader("Tu estratega de crecimiento con IA")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Mensaje de la IA - Versión Profesional
    with st.chat_message("assistant"):
        st.markdown("""
        **AI Growth Copilot:** Hola equipo, he detectado **12 carritos abandonados** en la última hora. 
        Tras analizar el **comportamiento de compra y el stock disponible**, el algoritmo ha determinado 
        que el cupón **GROWTH10** es la estrategia óptima para recuperar el 22% de estas ventas. 
        
        ¿Deseas activarlo ahora?
        """)
    
    st.write("")
    if st.button("🎯 Activar Estrategia de Recuperación"):
        with st.status("Sincronizando con Tiendanube API...", expanded=True) as status:
            st.write("Analizando comportamiento de productos...")
            time.sleep(1)
            st.write("Creando cupón dinámico GROWTH10...")
            time.sleep(1)
            status.update(label="¡Sincronización Exitosa!", state="complete", expanded=False)
        
        st.balloons()
        st.success("### ✅ ¡CUPÓN 'GROWTH10' CREADO EXITOSAMENTE!")

    # --- SECCIÓN DE PRODUCTOS ---
    st.write("---")
    st.markdown("### 📦 Análisis de Productos (Top Abandonados)")
    
    chart_data = pd.DataFrame({
        "Productos": [
            "Cámara de Seguridad WiFi", 
            "Sensor de Movimiento Pro", 
            "Kit de Primeros Auxilios", 
            "Cerradura Inteligente"
        ],
        "Vistos": [120, 95, 80, 45],
        "Abandonados": [42, 28, 15, 10]
    })
    
    st.bar_chart(chart_data.set_index("Productos"))
    st.caption("Filtro: Productos con mayor tasa de abandono en checkout (Últimas 24h).")

with col_right:
    st.markdown("### 📊 Métricas de Impacto")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Tasa de Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### 🏷️ Inteligencia de Precios")
    st.info("Tu precio promedio está **3% por debajo** de la competencia. Oportunidad de ajuste.")
    
    st.write("---")
    st.markdown("#### Tendencia de Recuperación")
    tendencia_data = np.random.randn(20, 1).cumsum()
    st.area_chart(tendencia_data)
    
    st.divider()
    st.markdown("### 👥 Equipo 3")
    
    # Lista de integrantes con apellidos y skills
    equipo = [
        ("Dalia Paola Rodríguez Trejo", "Capitana / Comunicación"),
        ("William Álvarez Carmona", "Lead Architect "),
        ("Montserrat Garcia Barona", "Fotografía / Redacción"),
        ("Jiram Cabrera Ramos", "Organización"),
        ("Cesar Augusto Fernandez Delgado", "Estrategia / Operaciones"),
        ("Edwing Garcia Juarez", "Ventas / Publicidad / Comunicación"),
        ("Carlos Andrés Almeida Rangel", "Liderazgo / Organización"),
        ("Amarilis Elizabeth Vera García", "Gestión / Análisis")
    ]
    
    for nombre, skill in equipo:
        st.markdown(f"**{nombre}**")
        st.caption(f"_{skill}_")

st.write("---")
st.caption("AI Growth Copilot | Hackathon UTEL 2026 - Equipo 3")
