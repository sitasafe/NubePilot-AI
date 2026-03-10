import streamlit as st
import pandas as pd
import requests  # Importante para conectar con la API

# 1. Configuración de la página
st.set_page_config(
    page_title="NubePilot AI | Equipo 3",
    page_icon="🚀",
    layout="centered"
)

# --- CONFIGURACIÓN DE LA API (Punto 1 y 3 de la Biblia) ---
# William: Aquí es donde pondrás los datos reales cuando crees tu App en el partner de Tiendanube
STORE_ID = "123456" # Ejemplo
ACCESS_TOKEN = "TU_ACCESS_TOKEN" # Ejemplo
API_URL = f"https://api.tiendanube.com/2025-03/{STORE_ID}/"

headers = {
    'Authentication': f'bearer {ACCESS_TOKEN}',
    'User-Agent': 'NubePilotAI (equipo3@hackathon.com)', # Obligatorio
    'Content-Type': 'application/json'
}

# --- FUNCIÓN PARA OBTENER DATOS REALES (Punto 2 de la Biblia) ---
def obtener_carritos_abandonados():
    # En un escenario real, aquí llamaríamos a: API_URL + "checkouts"
    # Por ahora, simulamos la respuesta exitosa para que la app no truene
    return 12 

# ---------------------------------------------------------

# 2. Título y Subtítulo
st.title("🚀 NubePilot AI")
st.subheader("Tu Copiloto de Crecimiento Inteligente para Tiendanube")

# 3. Resumen de métricas (Usando la lógica de la API)
st.write("---")
st.markdown("### 📊 Estado Actual de la Tienda")
col1, col2, col3 = st.columns(3)

cantidad_abandonos = obtener_carritos_abandonados()

col1.metric("Carritos Abandonados", f"{cantidad_abandonos}", "↑ 2")
col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
col3.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200", delta_color="inverse")

st.write("---")

# 4. Sección de IA con lógica de "Coupons" (Punto 2 de la Biblia)
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight detectado:** El 60% de los abandonos ocurren por el costo de envío.")

if st.button("Generar Estrategia de Recuperación"):
    st.balloons()
    st.success("✅ **Estrategia enviada a la API de Tiendanube:**")
    st.write(f"Se ha creado un cupón dinámico para los {cantidad_abandonos} carritos detectados.")
    
    # Aquí es donde integraríamos el POST a /coupons
    st.code(f"""
    POST /2025-03/{STORE_ID}/coupons
    {{
        "code": "ENVIOGRATIS3",
        "type": "percentage",
        "value": "100"
    }}
    """, language="json")
    
    st.write("- **Estado:** Cupón 'ENVIOGRATIS3' activado en la tienda.")

st.write("---")

# 5. Gráfico de Tendencia
st.markdown("### 📈 Impacto Estimado de NubePilot")
chart_data = [10, 20, 15, 40, 50, 65, 80]
st.line_chart(chart_data)

st.write("---")

# 6. Tabla de Productos (Punto 2 de la Biblia - Resources: Product)
st.markdown("### 🛒 Productos con más Abandonos")
data = {
    "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
    "Abandonos": [8, 3, 1],
    "Perdida Est.": ["$800 MXN", "$450 MXN", "$250 MXN"]
}
st.table(pd.DataFrame(data))

# 7. Barra lateral
st.sidebar.image("https://img.icons8.com/fluency/100/bot.png")
st.sidebar.title("Panel de Control")
st.sidebar.write("**Status:** Conexión API Preparada 🟢")
st.sidebar.write(f"**API Versión:** 2025-03")
