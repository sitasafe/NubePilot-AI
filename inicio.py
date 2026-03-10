# --- COPIA ESTO EN TU GITHUB ---
import streamlit as st
import requests

st.set_page_config(page_title="NubePilot AI", page_icon="🚀")
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# Inicializar token en la sesión para que no se pierda
if 'final_token' not in st.session_state:
    st.session_state['final_token'] = ""

st.sidebar.title("⚙️ Panel de Control")

with st.sidebar.expander("🔑 Generador de Access Token", expanded=True):
    temp_code = st.text_input("Pega el 'Code' de Partners")
    if st.button("Generar Token"):
        params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": temp_code.strip()}
        res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=params)
        if res.status_code == 200:
            st.session_state['final_token'] = res.json().get('access_token')
            st.success("¡Token Creado y Vinculado! ✅")
        else:
            st.error("Error al generar. Obtén un nuevo Code de Partners.")

st.sidebar.markdown("---")
# Este campo ahora se llena solo cuando generas el token arriba
api_token = st.sidebar.text_input("Access Token de API", value=st.session_state['final_token'], type="password")
user_id = st.sidebar.text_input("ID de Tienda", value="2831942")

st.title("🚀 NubePilot AI")
if st.button("🎯 Activar Estrategia"):
    if not api_token:
        st.error("Primero genera el token en la barra lateral.")
    else:
        # Probamos la URL más estable
        url = f"https://api.tiendanube.com/v1/{user_id}/coupons"
        headers = {"Authentication": f"bearer {api_token.strip()}", "Content-Type": "application/json", "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"}
        payload = {"code": "SITASAFE10", "type": "percentage", "value": "10", "max_uses": 50}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [201, 200]:
            st.balloons()
            st.success("### ✅ ¡LOGRADO! Cupón creado.")
        elif response.status_code == 422:
            st.warning("⚠️ El cupón ya existe (La conexión es exitosa).")
        else:
            st.error(f"Error {response.status_code}. Intenta generar un nuevo token.")
