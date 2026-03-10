import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Sitasafe", page_icon="🚀", layout="wide")

# --- DATOS DE TU APP ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
# Versión de la API según la documentación que enviaste
API_VERSION = "2025-03" 

# --- BARRA LATERAL ---
st.sidebar.title("⚙️ Panel de Control")

# Generador de Token (Mantenlo por si necesitas refrescar en vivo)
with st.sidebar.expander("🔑 Generador de Access Token"):
    temp_code = st.text_input("Pega el 'Code' de Partners")
    if st.button("Generar Token"):
        res = requests.post("https://www.tiendanube.com/apps/authorize/token", 
                            json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, 
                                  "grant_type": "authorization_code", "code": temp_code.strip()})
        if res.status_code == 200:
            st.code(res.json().get('access_token'))
            st.success("¡Token creado!")

st.sidebar.markdown("---")
# Pega aquí el token que empieza con 2b74...
api_token = st.sidebar.text_input("Access Token de API", value="2b747fc9c453d3af721cd12862026eeb55848e6c", type="password")
user_id = st.sidebar.text_input("ID de Tienda", value="2831942")

# --- CUERPO PRINCIPAL ---
st.title("🚀 NubePilot AI")
st.info("**IA:** William, he detectado carritos abandonados. ¿Creamos el cupón **SITASAFE10** ahora?")

if st.button("🎯 Activar Estrategia"):
    if not api_token:
        st.error("Falta el Token.")
    else:
        # URL ACTUALIZADA A VERSION 2025-03
        url = f"https://api.tiendanube.com/{API_VERSION}/{user_id}/coupons"
        
        headers = {
            "Authentication": f"bearer {api_token.strip()}",
            "Content-Type": "application/json",
            "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
        }
        
        payload = {
            "code": "SITASAFE10",
            "type": "percentage",
            "value": "10",
            "max_uses": 50
        }
        
        with st.spinner("Conectando con la API v2025-03..."):
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                st.balloons()
                st.success("✅ ¡Cupón Creado Exitosamente!")
            elif response.status_code == 401:
                st.error("❌ Error 401: Token inválido para la versión 2025-03.")
            elif response.status_code == 422:
                st.warning("⚠️ El cupón ya existe en la tienda.")
            else:
                st.error(f"Error {response.status_code}")
                st.json(response.json())
