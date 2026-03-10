import streamlit as st
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# Mantener el token en la sesión
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚙️ Configuración")
    temp_code = st.text_input("Código de Instalación (de Partners)")
    
    if st.button("Generar Access Token"):
        if temp_code:
            token_params = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": temp_code.strip()
            }
            res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=token_params)
            if res.status_code == 200:
                st.session_state['access_token'] = res.json().get('access_token')
                st.success("¡Token vinculado! ✅")
            else:
                st.error("Error: El código expiró.")
        else:
            st.warning("Ingresa el código.")

    st.markdown("---")
    user_id = st.text_input("ID de la Tienda", value="2831942")

# --- CUERPO PRINCIPAL ---
st.title("🚀 NubePilot AI")
st.markdown("### *Tu estratega de crecimiento con IA*")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Asesor Inteligente (Modo Chat)")
    
    with st.chat_message("assistant"):
        st.write("Hola William, analicé tu tienda **Sitasafe**. He detectado **12 carritos abandonados**.")
        st.write("**Recomendación:** Crea un cupón de descuento 'SITASAFE10'.")

    if st.button("🎯 Ejecutar Recomendación: Crear Cupón"):
        if not st.session_state['access_token']:
            st.error("❌ Error: Falta el token en la barra lateral.")
        else:
            api_url = f"https://api.tiendanube.com/2025-03/{user_id}/coupons"
            api_headers = {
                "Authentication": f"bearer {st.session_state['access_token']}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            api_payload = {
                "code": "SITASAFE10",
                "type": "percentage",
                "value": "10",
                "max_uses": 50
            }

            with st.spinner("Conectando con Tiendanube..."):
                try:
                    response = requests.post(api_url, headers=api_headers, json=api_payload)
                    if response.status_code == 201:
                        st.balloons()
                        st.success("### ¡Éxito! Cupón creado en la tienda.")
                    elif response.status_code == 422:
                        st.warning("El cupón ya existe.")
                    else:
                        st.error(f"Error {response.status_code}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

with col2:
    st.subheader("📊 Métricas Clave")
    st.metric(label="Ventas Recuperables", value="$450.00", delta="+12%")
    st.metric(label="Tasa de Conversión", value="3.5%", delta="0.8%")
