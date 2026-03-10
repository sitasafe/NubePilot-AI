import streamlit as st
import pandas as pd

# 1. Configuración de la página (Título en la pestaña y Layout)
st.set_page_config(
    page_title="NubePilot AI | Equipo 3",
    page_icon="🚀",
    layout="centered"
)

# 2. Título y Subtítulo
st.title(" NubePilot AI")
st.subheader("Tu Copiloto de Crecimiento Inteligente para Tiendanube")

# 3. Resumen de métricas principales (Estado de la Tienda)
st.write("---")
st.markdown("### 📊 Estado Actual de la Tienda")
col1, col2, col3 = st.columns(3)

# Datos basados en la validación del "Tío" y el equipo
col1.metric("Carritos Abandonados", "12", "↑ 2")
col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
col3.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200", delta_color="inverse")

st.write("---")

# 4. Sección de Inteligencia Artificial (El núcleo del proyecto)
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight detectado:** El 60% de los abandonos ocurren en el paso de 'Costo de Envío'.")

if st.button("Generar Estrategia de Recuperación"):
    st.balloons()
    st.success("✅ **Estrategia Optimizada por IA:**")
    st.write("Se ha detectado que el producto **'Playera Algodón'** tiene alta intención de compra pero se abandona al final.")
    st.write("- **Acción:** Crear cupón de envío gratis: **ENVIOGRATIS3**")
    st.write("- **Canal:** Enviar vía WhatsApp Automatizado en 15 minutos.")
    st.code("Cupón: ENVIOGRATIS3 | Status: Programado", language="bash")

st.write("---")

# 5. Gráfico de Tendencia de Recuperación
st.markdown("### 📈 Impacto Estimado de NubePilot")
st.write("Proyección de recuperación de ventas al aplicar las estrategias de la IA:")
chart_data = [10, 20, 15, 40, 50, 65, 80] # Simulación de éxito
st.line_chart(chart_data)

st.write("---")

# 6. Tabla de Productos Críticos
st.markdown("### 🛒 Productos con más Abandonos")
st.write("Detalle de productos que requieren atención inmediata:")
data = {
    "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
    "Abandonos": [8, 3, 1],
    "Perdida Est.": ["$800 MXN", "$450 MXN", "$250 MXN"]
}
df = pd.DataFrame(data)
st.table(df)

# 7. Barra lateral de estado
st.sidebar.image("https://img.icons8.com/fluency/100/bot.png")
st.sidebar.title("Panel de Control")
st.sidebar.write("**Equipo:** Equipo 3")
st.sidebar.write("**Tienda:** Prueba Tío (Validada)")
st.sidebar.write("**Status:** API Tiendanube Conectada")
st.sidebar.divider()
st.sidebar.write("© 2026 Hackathon Universitario")