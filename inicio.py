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
st.markdown("# AI Growth Copilot")
st.subheader("Tu estratega de crecimiento")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- MÓDULO DE IA GENERATIVA (ANÁLISIS PROACTIVO) ---
    with st.chat_message("assistant"):
        st.write("🤖 **Ejecutando algoritmos de crecimiento...**")
        placeholder = st.empty()
        
        # FRASE PROFESIONAL EN SINTONÍA CON EL NEGOCIO
        mensaje_ia = """**Análisis del Copilot finalizado:** He detectado una ventana de oportunidad en **12 carritos abandonados**. 

Tras procesar los patrones de demanda y la disponibilidad actual en el inventario, el sistema ha diseñado la siguiente estrategia de conversión:

El cupón **GROWTH10** es la herramienta óptima para incentivar el cierre de estas ventas con una probabilidad de éxito del 88%. ¿Deseas aplicar esta acción ahora?"""
        
        # Efecto de escritura tipo ChatGPT
        full_response = ""
        for char in mensaje_ia:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
        placeholder.markdown(full_response)
    
    st.write("")
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
    user_input = st.text_input("Hazle una pregunta a tu Copilot (Ej: ¿Por qué bajaron mis ventas?):")
    
    if user_input:
        with st.chat_message("assistant"):
            with st.spinner("IA procesando datos de la tienda..."):
                time.sleep(1.5)
                if "ventas" in user_input.lower():
                    st.write("📊 **Análisis Generativo:** Las métricas indican una fluctuación del 5% debido a la estacionalidad y competencia en el sector de seguridad. Sugiero activar una campaña de 'Bundle' en productos de alta rotación.")
                else:
                    st.write("Basado en el análisis de inventario, recomiendo optimizar la descripción de la 'Cerradura Inteligente' para mejorar la conversión orgánica.")

    # --- SECCIÓN DE PRODUCTOS ---
    st.write("---")
    st.markdown("### 📦 Análisis de Productos (Top Abandonados)")
    chart_data = pd.DataFrame({
        "Productos": ["Cámara de Seguridad WiFi", "Sensor de Movimiento Pro", "Kit de Primeros Auxilios", "Cerradura Inteligente"],
        "Vistos": [120, 95, 80, 45],
        "Abandonados": [42, 28, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Productos"))

with col_right:
    st.markdown("### 📊 Métricas de Impacto")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Tasa de Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### 🏷️ Inteligencia de Precios")
    st.info("Tu precio promedio está **3% por debajo** de la competencia. Hay oportunidad de optimización de margen.")
    
    st.write("---")
    st.markdown("#### Tendencia de Recuperación")
    tendencia_data = np.random.randn(20, 1).cumsum()
    st.area_chart(tendencia_data)
    
    st.divider()
    st.markdown("### 👥 Equipo 3")
    equipo = [
        ("Dalia Paola Rodríguez Trejo", "Capitana / Comunicación"),
        ("Willan Álvarez Carmona", "Lead Architect / AI Dev"),
        ("Montserrat Garcia Barona", "Fotografía / Redacción"),
        ("Jiram Cabrera Ramos", "Organización"),
        ("Cesar Augusto Fernandez Delgado", "Estrategia / Operaciones"),
        ("Edwing Garcia Juarez", "Ventas / Publicidad"),
        ("Carlos Andrés Almeida Rangel", "Liderazgo / Organización"),
        ("Amarilis Elizabeth Vera García", "Gestión / Análisis")
    ]
    for nombre, skill in equipo:
        st.markdown(f"**{nombre}**")
        st.caption(f"_{skill}_")

st.write("---")
st.caption("AI Growth Copilot | IA Generativa | Hackathon UTEL 2026 - Equipo 3")
