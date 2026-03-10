import streamlit as st
import pandas as pd

# 1. Configuración de la página (Título en la pestaña y Layout)
st.set_page_config(
    page_title="NubePilot AI | Equipo 3",
    page_icon="🚀",
    layout="centered"
)

# --- VARIABLES DE CONFIGURACIÓN (Basado en API 2025-03) ---
STORE_ID = "123456" 
# ---------------------------------------------------------

# 2. Título y Subtítulo
st.title("🚀 NubePilot AI")
st.subheader("Tu Copiloto de Crecimiento Inteligente para Tiendanube")

# 3. Resumen de métricas principales (Estado de la Tienda)
st.write("---")
st.markdown("### 📊 Estado Actual de la Tienda")
col1, col2, col3 = st.columns(3)

# Datos validados con el equipo
col1.metric("Carritos Abandonados", "12", "↑ 2")
col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
col3.metric("Recuperación Est.", "$1,500 MXN", "+$200")

st.write("---")

# 4. Sección de Inteligencia Artificial (INTERFAZ HUMANA)
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight detectado:** Se detectó una alta tasa de abandono por falta de cupones de bienvenida.")

if st.button("Generar Estrategia de Recuperación"):
    st.balloons()
    
    # Mensaje de éxito amigable para el usuario
    st.success("✅ **¡Estrategia Activada con Éxito!**")
    
    st.markdown(f"""
    ### 📋 ¿Qué acaba de pasar?
    N
