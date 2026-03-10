import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Sitasafe", page_icon="🚀", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #0084FF; color: white; }
    .status-box { padding: 20px; border-radius: 10px; background-color: white; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (CONFIGURACIÓN TÉCNICA) ---
st.sidebar.image("https://admin.tiendanube.com/static/img/logos/tiendanube-logo.png", width=150)
st.sidebar.title("⚙️ Panel de Control")

# 1. Credenciales fijas de tu App de Partner
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# 2. Generador de Token (Lo que usamos para obtener el acceso)
with st.sidebar.expander("🔑 Generador de Access Token"):
    temp_code = st.text_input("Pega el 'Code' de Tiendanube")
    if st.button("Obtener Token Real"):
        res = requests.post("https://www.tiendanube.com/apps/authorize/token", 
                            json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, 
                                  "grant_type": "authorization_code", "code": temp_code.strip()})
        if res.status_code == 200:
            st.success(f"Token: {res.json().get('access_token')}")
        else:
            st.error("Código expirado o inválido")

# 3. Campos de conexión
api_token = st.sidebar.text_input("Access Token de API", type="password", help="Pega aquí el shpat_...")
user_id = st.sidebar.text_input("ID de Tienda", value="2831942")

if api_token:
    st.sidebar.success("Estado: Conectado ✅")
else:
    st.sidebar.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🚀 NubePilot AI")
    st.subheader("Optimización Inteligente para Sitasafe")
    
    # Simulación de Chat con la IA
    container = st.container()
    with container:
        st.info("**IA:** Hola William, he detectado que el 15% de los carritos abandonados son de clientes que miraron las 'Cintas Reflectivas'. ¿Quieres activar un cupón de descuento para recuperarlos?")
        
    if st.button("🎯 Activar Estrategia de Recuperación"):
        if not api_token:
            st.error("Error: No hay Token de API configurado.")
        else:
            # LLAMADA REAL A LA API DE TIENDANUBE
            url = f"https://api.tiendanube.com/v1/{user_id}/coupons"
            headers = {
                "Authentication": f"bearer {api_token}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            data = {
                "code": "SITASAFE10",
                "type": "percentage",
                "value": "10",
                "min_price": "0",
                "max_uses": 50
            }
            
            with st.spinner("Conectando con Tiendanube..."):
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 201:
                    st.balloons()
                    st.success("✅ ¡Estrategia Activada! Cupón 'SITASAFE10' creado con éxito en tu tienda.")
                    st.confetti = True
                else:
                    st.error(f"Error al crear cupón: {response.status_code}")
                    st.write(response.text)

with col2:
    st.markdown("### 📊 Estadísticas en Vivo")
    st.metric(label="Ventas Hoy", value="$42,500", delta="+12%")
    st.metric(label="Carritos Activos", value="18", delta="-2")
    
    st.markdown("---")
    st.markdown("### 🛠️ Próximas Tareas")
    st.checkbox("Optimizar SEO de 'Chalecos'", value=True)
    st.checkbox("Email marketing para clientes VIP", value=False)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("NubePilot AI v1.0 | Hackathon 2026 | Desarrollado para Sitasafe")
