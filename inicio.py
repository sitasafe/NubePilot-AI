import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="NubePilot AI - Sitasafe", page_icon="🚀", layout="wide")
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- BARRA LATERAL ---
st.sidebar.title("⚙️ Panel de Control")

with st.sidebar.expander("🔑 Generador de Access Token"):
    temp_code = st.text_input("Pega el 'Code' de Partners")
    if st.button("Generar Token"):
        params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": temp_code.strip()}
        res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=params)
        if res.status_code == 200:
            st.code(res.json().get('access_token'))
            st.success("¡Token Creado! Cópialo abajo.")
        else:
            st.error(f"Error {res.status_code}")

st.sidebar.markdown("---")
api_token = st.sidebar.text_input("Access Token de API", type="password")
user_id = st.sidebar.text_input("ID de Tienda", value="2831942")

# --- CUERPO ---
st.title("🚀 NubePilot AI")

if st.button("🎯 Activar Estrategia"):
    if not api_token:
        st.error("Pega el token generado arriba.")
    else:
        # PRUEBA CON LA URL QUE FUNCIONA SEGURO (V1)
        # A veces la v2025-03 falla si la app no tiene permisos específicos
        url = f"https://api.tiendanube.com/v1/{user_id}/coupons"
        
        # EL SECRETO: El header 'Authentication' debe ser exacto
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
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code in [201, 200]:
                st.balloons()
                st.success("### ✅ ¡ÉXITO! Cupón creado en Sitasafe.")
            elif response.status_code == 401:
                # Si falla la v1, intentamos la v2025-03 automáticamente
                url_v2 = f"https://api.tiendanube.com/2025-03/{user_id}/coupons"
                response = requests.post(url_v2, headers=headers, json=payload)
                if response.status_code == 201:
                    st.balloons()
                    st.success("### ✅ ¡ÉXITO (v2025-03)!")
                else:
                    st.error(f"Error 401 persistente. Revisa que el ID {user_id} sea el correcto de tu tienda de prueba.")
            elif response.status_code == 422:
                st.warning("⚠️ El cupón ya existe. ¡La conexión funciona!")
            else:
                st.error(f"Error {response.status_code}")
                st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")
