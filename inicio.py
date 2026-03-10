import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN DE TU APP (PARTNERS)
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- INICIALIZACIÓN DE VARIABLES (SESSION STATE) ---
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""

if 'code_usado' not in st.session_state:
    st.session_state['code_usado'] = ""

# --- BARRA LATERAL (RECUPERANDO EL DISEÑO QUE TE GUSTABA) ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    # Menú desplegable "Generador de Access Token" con el logo de la llave 🔑
    with st.expander("🔑 Generador de Access Token"):
        st.write("---")
        temp_code = st.text_input("Pega el 'Code' de Partners", help="Solo el código después de ?code=")
        
        # Guardamos el código que se va a usar para evitar errores si el usuario cambia el input
        st.session_state['code_usado'] = temp_code

        # Botón de "Generar Token"
        st.write("---")
        if st.button("Generar Token"):
            if st.session_state['code_usado']:
                token_params = {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": st.session_state['code_usado'].strip()
                }
                res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=token_params)
                
                if res.status_code == 200:
                    st.session_state['access_token'] = res.json().get('access_token')
                    st.success("¡Token Creado! Cópialo y pégalo abajo. ✅")
                    # Mostramos el token para copiar (Cuadro gris con icono)
                    st.code(st.session_state['access_token'])
                else:
                    st.error("Error: El código expiró.")
            else:
                st.warning("Escribe el código primero.")

    st.write("---")
    
    # Campo "Access Token de API" (Oculto como en image_1.png)
    token_api = st.text_input("Access Token de API", type="password", value=st.session_state['access_token'], help="Pega aquí el token generado arriba")
    
    st.write("---")
    
    # Campo "ID de Tienda"
    id_tienda = st.text_input("ID de Tienda", value="2831942")

st.markdown("---")

# --- CUERPO PRINCIPAL ---
st.markdown("# 🚀 NubePilot AI")
st.markdown("### *Tu estratega de crecimiento con IA*")

# Simulamos la Inteligencia de la IA
st.write("---")
col_info, col_chart = st.columns([2, 1])

with col_info:
    # Simulación del Chat de la IA que te gustaba
    with st.chat_message("assistant"):
        st.markdown(f"**IA:** Hola William, analicé tu tienda Sitasafe. He detectado 12 carritos abandonados. ¿Activamos el cupón **SITASAFE10**?")
    
    # Botón de "🎯 Activar Estrategia" (El original que funciona)
    if st.button("🎯 Activar Estrategia"):
        if not token_api:
            st.error("❌ Error: Primero genera y pega el Access Token en la barra lateral.")
        else:
            api_url = f"https://api.tiendanube.com/2025-03/{id_tienda}/coupons"
            api_headers = {
                "Authentication": f"bearer {token_api.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            api_payload = {
                "code": "SITASAFE10",
                "type": "percentage",
                "value": "10",
                "max_uses": 50
            }

            with st.spinner("Sincronizando con Tiendanube..."):
                try:
                    response = requests.post(api_url, headers=api_headers, json=api_payload)
                    if response.status_code == 201:
                        st.balloons()
                        st.success("### ✅ ¡ÉXITO! Cupón 'SITASAFE10' creado automáticamente en Sitasafe.")
                    elif response.status_code == 4
