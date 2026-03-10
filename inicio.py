import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="NubePilot AI | Equipo 3",
    page_icon="🚀",
    layout="centered"
)

# --- VARIABLES DE CONFIGURACIÓN ---
STORE_ID = "123456" 

# 2. Título y Subtítulo
st.title("🚀 NubePilot AI")
st.subheader("Tu Copiloto de Crecimiento Inteligente para Tiendanube")

# 3. Resumen de métricas principales
st.write("---")
st.markdown("### 📊 Estado Actual de la Tienda")
col1, col2, col3 = st.columns(3)

col1.metric("Carritos Abandonados", "12", "↑ 2")
col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
col3.metric("Recuperación Est.", "$1,500 MXN", "+$200")

st.write("---")

# 4. Sección de Inteligencia Artificial (INTERFAZ HUMANA)
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight detectado:** Se detectó una alta tasa de abandono por falta de cupones de bienvenida.")

if st.button("Generar Estrategia de Recuperación"):
    st.balloons()
    st.success("✅ **¡Estrategia Activada con Éxito!**")
    
    # AQUÍ ESTABA EL ERROR: Aseguramos cerrar correctamente con """
    st.markdown(f"""
