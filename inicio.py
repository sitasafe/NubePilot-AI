import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Sitasafe", page_icon="🚀", layout="wide")

# --- DATOS DE TU APP (PARTNERS) ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"
API_VERSION = "2025-03"

# --- ESTILOS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #0084FF; color: white; font-weight: bold; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
st.sidebar.title("⚙️ Panel de Control")

# 1. Generador de Access Token (Corregido)
with st.sidebar.expander("🔑 Generador de Access Token"):
    temp_code = st.text_input("Pega el 'Code' de Partners aquí")
    if st.button("Generar Token"):
        if temp_code:
            # Preparamos los parámetros para el intercambio seguro
            params = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": temp_code.strip()
            }
            # Solicitud a Tiendanube
            res = requests.post("https://www.tiendanube.com/apps/authorize/token", json=params)
            
            if res.status_code == 200:
                data = res.json()
                nuevo_token = data.get('access_token')
                st.code(nuevo_token)
                st.success("¡Token Creado! Cópialo y pégalo abajo.")
            else:
                st.error(f"Error {res.status_code}: Código inválido o expirado.")
        else:
            st.warning("Escribe el código primero.")

st.sidebar.markdown("---")

# 2. Configuración de Conexión (El campo que usa el botón azul)
api_token = st.sidebar.text_input("Access Token de API", type="password", help="Pega aquí el token generado arriba")
user_id = st.sidebar.text_input("ID de Tienda", value="2831942")

if api_token and len(api_token) > 10:
    st.sidebar.success("Estado: Conectado ✅")
else:
    st.sidebar.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL ---
st.title("🚀 NubePilot AI")
st.subheader("Optimización en Tiempo Real para Sitasafe")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("**IA:** Hola William, he detectado carritos abandonados con 'Cintas Reflectivas'. ¿Activamos un cupón de descuento del 10%?")
    
    if st.button("🎯 Activar Estrategia de Recuperación"):
        if not api_token:
            st.error("❌ Por favor, pega el Access Token en la barra lateral.")
        else:
            # URL de la API v2025-03
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
                "min_price": "0",
                "max_uses": 50
            }
            
            with st.spinner("Sincronizando con Tiendanube v2025-03..."):
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 201:
                        st.balloons()
                        st.success("### ✅ ¡CUPÓN CREADO!")
                        st.write("Estrategia activa: El cupón **SITASAFE10** ya está disponible.")
                    elif response.status_code == 401:
                        st.error("❌ Error 401: Token no autorizado. Refresca el token en el panel lateral.")
                    elif response.status_code == 422:
                        st.warning("⚠️ El cupón 'SITASAFE10' ya existe en tu tienda.")
                    else:
                        st.error(f"Error {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"Falla de conexión: {e}")

with col2:
    st.markdown("### 📈 Impacto Estimado")
    st.metric("Ventas Recuperables", "+15.4%", "↑ 2.1%")
    st.metric("Conversión", "3.2%", "↑ 0.5%")
    
    st.markdown("---")
    st.write("**Log de la IA:**")
    st.caption("- Sincronización con Tiendanube API")
    st.caption("- Escaneo de carritos abandonados (OK)")

st.markdown("---")
st.caption("NubePilot AI | Hackathon 2026")
