import streamlit as st
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN (No cambiar)
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# Mantener el token en la sesión para que no se borre al interactuar
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""

# --- BARRA LATERAL (CONTROL TÉCNICO) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    st.info("Paso 1: Genera tu token de acceso")
    
    temp_code = st.text_input("Código de Instalación (de Partners)", help="Pega el código que sale en la URL después de ?code=")
    
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
                st.success("¡Token vinculado correctamente! ✅")
            else:
                st.error("Error: El código expiró o es incorrecto.")
        else:
            st.warning("Ingresa el código primero.")

    st.markdown("---")
    user_id = st.text_input("ID de la Tienda", value="2831942")
    st.write(f"**Status:** {'Conectado ✅' if st.session_state['access_token'] else 'Desconectado ⚠️'}")

# --- CUERPO PRINCIPAL (INTERFAZ PARA EL EQUIPO) ---
st.title("🚀 NubePilot AI")
st.markdown("### *Tu estratega de crecimiento con IA*")

# Simulamos el análisis de la IA
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Asesor Inteligente (Modo Chat)")
    
    # Simulación de conversación que pidió el equipo
    with st.chat_message("assistant"):
        st.write("Hola William, analicé tu tienda **Sitasafe**. He detectado que tienes **12 carritos abandonados** en las últimas 24 horas. Esto representa una pérdida potencial de $450 USD.")
        st.write("**Recomendación:** Activa un cupón de descuento 'SITASAFE10' para incentivar el cierre de estas ventas.")

    # El botón de ACCIÓN REAL que te hace destacar
    if st.button("🎯 Ejecutar Recomendación: Crear Cupón"):
        if not st.session_state['access_token']:
            st.error("❌ Error: Primero debes generar el token en la barra lateral.")
        else:
            # URL de la API v2025-03
            url = f"https://api.tiendanube.com/2025-03/{user_id}/coupons"
            headers = {
                "Authentication": f"bearer {st.session_state['access_token']}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysit
