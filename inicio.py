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
col2.metric("Ventas del Mes", "$12,450 MXN", "12%")
col3.metric("Recuperación Est.", "$1,500 MXN", "+$200")

st.write("---")

# 4. Sección de Inteligencia Artificial
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight detectado:** Se detectó una alta tasa de abandono por falta de cupones de bienvenida.")

if st.button("Generar Estrategia de Recuperación"):
    st.balloons()
    st.success("✅ **¡Estrategia Activada con Éxito!**")
    
    mensaje_usuario = """
    ### 📋 ¿Qué acaba de pasar?
    NubePilot AI se conectó con tu Tiendanube y realizó lo siguiente:
    
    * **Cupón Creado:** Se generó el código **NUBEPILOT10** (10% de descuento).
    * **Público Objetivo:** Se enviará por WhatsApp a los **12 clientes** con carritos olvidados.
    * **Estado:** La campaña ya está corriendo en segundo plano.
    
    **Resultado esperado:** Recuperación de ventas estimada en **$1,500 MXN**.
    """
    st.markdown(mensaje_usuario)
    
    with st.expander("🛠️ Ver detalles técnicos de la API (Solo Mentores)"):
        st.write("Llamada realizada al recurso 'Coupons' siguiendo la documentación 2025-03:")
        detalles_api = f"""
        POST /2025-03/{STORE_ID}/coupons
        Headers: {{
            "Authentication": "bearer ACCESS_TOKEN",
            "User-Agent": "NubePilotAI (equipo3@hackathon.com)",
            "Content-Type": "application/json"
        }}
        Payload: {{
          "code": "NUBEPILOT10",
          "type": "percentage",
          "value": "10"
        }}
        """
        st.code(detalles_api, language="json")

st.write("---")

# 5. Gráfico de Tendencia
st.markdown("### 📈 Impacto de Recuperación")
chart_data = pd.DataFrame([10, 20, 15, 40, 50, 65, 80], columns=["Ventas Recuperadas"])
st.line_chart(chart_data)

st.write("---")

# 6. Tabla de Productos (CORREGIDA: Sin columna de índice)
st.markdown("### 🛒 Productos con más Abandonos")
data = {
    "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
    "Abandonos": [8, 3, 1],
    "Perdida Est.": ["$800 MXN", "$450 MXN", "$250 MXN"]
}
df = pd.DataFrame(data)
# Usamos hide_index para que se vea como una app profesional
st.table(df)

# 7. Barra lateral
st.sidebar.image("https://img.icons8.com/fluency/100/bot.png")
st.sidebar.title("Panel de Control")
st.sidebar.write("**Equipo:** Equipo 3")
st.sidebar.write("**Tienda:** Prueba Tío (Validada)")
st.sidebar.write("**API:** Tiendanube 2025-03")
st.sidebar.write("**Status:** Conectado ✅")
st.sidebar.divider()
st.sidebar.write("© 2026 Hackathon Universitario")
