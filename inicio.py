import streamlit as st
import requests

# Configuración inicial
st.title("🚀 NubePilot AI - Conexión Tiendanube")

# Datos de tu App de Partner (Los que ya tienes)
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

st.sidebar.header("🔌 Configuración de API")
code_temporal = st.sidebar.text_input("Pega aquí el 'Code' de Tiendanube")

if st.sidebar.button("Generar Access Token Real"):
    url_token = "https://www.tiendanube.com/apps/authorize/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code_temporal.strip()
    }
    
    response = requests.post(url_token, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        token_final = data.get("access_token")
        st.sidebar.success("✅ ¡Token Generado!")
        st.sidebar.code(token_final) # ESTO ES LO QUE PEGARÁS EN TU APP
    else:
        st.sidebar.error(f"Error: {response.status_code}. El código expiró.")
        st.sidebar.write("Vuelve a darle a 'Instalar' en Partners para un código nuevo.")
