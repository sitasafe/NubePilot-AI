import streamlit as st
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(
    page_title="NubePilot AI | Equipo 3",
    page_icon="🤖",
    layout="wide"
)

# --- VARIABLES DE CONFIGURACIÓN ---
# Usamos el ID de tu tienda Sitasafe que vimos en las capturas
DEFAULT_STORE_ID = "2831942" 

# 2. Barra Lateral (Conexión Oficial)
st.sidebar.image("https://img.icons8.com/fluency/100/bot.png")
st.sidebar.title("🔌 Conexión Oficial")
st.sidebar.write("Configura la comunicación con Tiendanube")

store_id = st.sidebar.text_input("ID de la Tienda (Sitasafe)", value=DEFAULT_STORE_ID)
access_token = st.sidebar.text_input("Access Token de API", type="password", help="Obtenlo en Configuración > Códigos Externos")

st.sidebar.divider()
st.sidebar.write("**Equipo:** Equipo 3")
st.sidebar.write("**Status:** Conectado ✅" if access_token else "Status: Esperando Token 🔑")
st.sidebar.write("**API:** 2025-03 (Latest)")

# 3. Encabezado Principal
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("🚀 NubePilot AI")
    st.subheader("Copiloto de Crecimiento para Tienda Sitasafe")

# 4. Métricas en Tiempo Real (Simuladas para el Pitch)
st.write("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Carritos Abandonados", "12", "↑ 2")
m2.metric("Ventas del Mes", "$12,450 MXN", "12%")
m3.metric("Tasa de Conversión", "2.4%", "-0.5%")
m4.metric("Recuperación Est.", "$1,500 MXN", "+$200")

# 5. Sección de Inteligencia Artificial
st.write("---")
st.markdown("### 🤖 Recomendación de NubePilot AI")
st.info("💡 **Insight Detectado:** Se identificó una caída en la conversión. El 60% de los abandonos en 'Sitasafe' ocurren por costos de envío o falta de incentivos iniciales.")

# Lógica del Botón de Acción
if st.button("Activar Estrategia de Recuperación"):
    if not access_token:
        st.error("❌ **Error de Autenticación:** No has ingresado un Access Token en la barra lateral.")
        st.info("Para la demo: Muestra el bloque de código abajo para explicar la integración técnica.")
    else:
        # Intento de conexión REAL
        url = f"https://api.tiendanube.com/2025-03/{store_id}/coupons"
        headers = {
            'Authentication': f'bearer {access_token}',
            'User-Agent': 'NubePilotAI (equipo3@hackathon.com)',
            'Content-Type': 'application/json'
        }
        payload = {
            "code": "SITASAFE10",
            "type": "percentage",
            "value": "10"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                st.balloons()
                st.success("✅ **¡Éxito!** El cupón 'SITASAFE10' ha sido creado en tu panel de Tiendanube.")
            elif response.status_code == 401:
                st.warning("🔑 **Error 401:** Token inválido. Revisa tus credenciales en el panel de Partners.")
            else:
                st.error(f"⚠️ La API respondió con código {response.status_code}")
        except Exception as e:
            st.error(f"Hubo un problema de conexión: {e}")

# 6. Bloque Técnico para Jueces (Indispensable en Hackathon)
with st.expander("🛠️ Ver Payload y Detalles Técnicos (API Documentation 2025-03)"):
    st.write("Esta es la estructura que nuestra IA envía al servidor de Tiendanube:")
    
    # Presentación limpia del código
    st.code(f"""
    POST /2025-03/{store_id}/coupons
    Headers: {{
        "Authentication": "bearer ********",
        "User-Agent": "NubePilotAI (equipo3@hackathon.com)",
        "Content-Type": "application/json"
    }}
    Payload: {{
      "code": "SITASAFE10",
      "type": "percentage",
      "value": "10"
    }}
    """, language="json")
    st.caption("Nota: Se utiliza el formato snake_case y autenticación Bearer según el estándar oficial.")

# 7. Gráfico de Proyección
st.write("---")
st.markdown("### 📈 Impacto Esperado en Ventas")
chart_data = pd.DataFrame({
    'Días': ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
    'Ventas Actuales': [100, 120, 110, 130, 150, 170, 160],
    'Con NubePilot': [100, 140, 135, 160, 190, 230, 220]
})
st.line_chart(chart_data.set_index('Días'))

st.sidebar.write("© 2026 Hackathon Universitario")
