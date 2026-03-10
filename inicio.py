import streamlit as st
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="NubePilot AI | Equipo 3", page_icon="🚀")

# 2. Sidebar para conexión real
st.sidebar.title("🔌 Conexión Oficial")
store_id = st.sidebar.text_input("ID de tu Tienda (Sitasafe)", value="2831942") # Cambia este num por el tuyo
access_token = st.sidebar.text_input("Access Token de API", type="password")

# 3. Encabezados según la documentación oficial
headers = {
    'Authentication': f'bearer {access_token}',
    'User-Agent': 'NubePilotAI (equipo3@hackathon.com)',
    'Content-Type': 'application/json'
}

st.title("🚀 NubePilot AI")
st.info("💡 **Insight:** Baja conversión en 'Tienda de Sitasafe. Code'. Se recomienda campaña de cupones.")

# 4. Botón de ejecución REAL
if st.button("Activar Estrategia en Tiendanube"):
    if not access_token:
        st.warning("⚠️ Por favor, ingresa el Token en la barra lateral para conectar con Sitasafe.")
    else:
        url = f"https://api.tiendanube.com/2025-03/{store_id}/coupons"
        payload = {
            "code": "SITASAFE10",
            "type": "percentage",
            "value": "10"
        }
        
        # Intentar crear el cupón real en tu tienda
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                st.success("✅ ¡Cupón 'SITASAFE10' creado exitosamente en tu tienda!")
                st.balloons()
            else:
                st.error(f"Error de API: {response.status_code} - Revisa tus permisos.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

# 5. Visualización técnica para los jueces
with st.expander("🛠️ Ver Payload enviado a Tiendanube"):
    st.code(f"POST /2025-03/{store_id}/coupons\nContent-Type: application/json", language="bash")
    st.json({"code": "SITASAFE10", "type": "percentage", "value": "10"})
