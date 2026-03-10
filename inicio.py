import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# Inicializar sesión
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = ""

# --- BARRA LATERAL (EL DISEÑO QUE TE GUSTA) ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Generador de Access Token", expanded=True):
        temp_code = st.text_input("Pega el 'Code' de Partners")
        if st.button("Generar Token"):
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
                    st.success("¡Token Creado! ✅")
                    st.code(st.session_state['access_token'])
                else:
                    st.error("Error: Code expirado.")
            else:
                st.warning("Escribe el código.")

    st.write("---")
    token_api = st.text_input("Access Token de API", type="password", value=st.session_state['access_token'])
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if token_api:
        st.sidebar.success("Estado: Conectado ✅")
    else:
        st.sidebar.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL (DINÁMICO) ---
st.title("🚀 NubePilot AI")
st.subheader("Optimización en Tiempo Real para Sitasafe")
st.write("---")

col_main, col_side = st.columns([2, 1])

with col_main:
    with st.chat_message("assistant"):
        st.markdown("**IA:** Hola William, he detectado carritos abandonados. ¿Activamos el cupón del 10%?")
    
    if st.button("🎯 Activar Estrategia"):
        if not token_api:
            st.error("❌ Falta el Access Token en el panel lateral.")
        else:
            url = f"https://api.tiendanube.com/2025-03/{id_tienda}/coupons"
            headers = {
                "Authentication": f"bearer {token_api.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            payload = {"code": "SITASAFE10", "type": "percentage", "value": "10", "max_uses": 50}
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 201:
                    st.balloons()
                    st.success("### ✅ ¡CUPÓN CREADO!")
                elif response.status_code == 422:
                    st.warning("⚠️ El cupón ya existe en la tienda.")
                else:
                    st.error(f"Error {response.status_code}")
            except Exception as e:
                st.error(f"Falla: {e}")

with col_side:
    st.markdown("### 📊 Métricas Clave")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### **Equipo 10:**")
    st.caption("👤 **William L.** (Lead Architect)")
    st.caption("👤 **Dalia** (Product Manager)")
    st.caption("👤 **Montse** (Strategy)")
    st.caption("👤 **Integrantes Equipo 10**")

st.write("---")
st.caption("NubePilot AI | Hackathon 2026")
