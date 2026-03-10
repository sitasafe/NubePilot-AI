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
            payload = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": temp_code.strip()
            }
            res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=payload)
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
            url = f"https://api.tiendanube.com/2025-03/{user_id}/coupons"
            headers = {
                "Authentication": f"bearer {st.session_state['access_token']}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            payload = {
                "code": "SITASAFE10",
                "type": "percentage",
                "value": "10",
                "max_uses": 50
