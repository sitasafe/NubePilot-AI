import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Sitasafe", page_icon="🚀", layout="wide")

# --- ESTILOS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #0084FF; color: white; font-weight: bold; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS DE TU APP (PARTNERS) ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- BARRA LATERAL ---
st.sidebar.image("https://admin.tiendanube.com/static/img/logos/tiendanube-logo.png", width=150)
st.sidebar.title("⚙️ Panel de Control")

# 1. Generador de Token (Para emergencias)
with st.sidebar.expander("🔑 Generador de Access Token"):
    temp_code = st.text_input("Pega aquí el nuevo 'Code'")
    if st.button("Generar Nuevo Token"):
        if temp_code:
            res = requests.post("https://www.tiendanube.com/apps/authorize/token", 
                                json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, 
                                      "grant_type": "authorization_code", "code": temp_code.strip()})
            if res.status_code == 200:
                nuevo_token = res.json().get('access_token')
                st.success("¡Token Generado!")
                st.code(nuevo_token)
            else:
                st.error(f"Error: {res.status_code}")
        else:
            st.warning("Escribe un código primero")

# 2. Configuración de Conexión
st.sidebar.markdown("---")
# Pega aquí el token que ya tienes si quieres que quede fijo
api_token = st.sidebar.text_input("Access Token de API", value="2b747fc9c453d3af721cd12862026eeb55848e6c", type="password")
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
    st.info("**IA:** Hola William, detecté que muchos clientes abandonan carritos con 'Cintas Reflectivas'. ¿Activamos un cupón de descuento del 10%?")
    
    if st.button("🎯 Activar Estrategia de Recuperación"):
        if not api_token:
            st.error("❌ Falta el Access Token en la barra lateral.")
        else:
            # LLAMADA A LA API DE TIENDANUBE
            url = f"https://api.tiendanube.com/v1/{user_id}/coupons"
            
            # CABECERAS CORREGIDAS PARA EVITAR ERROR 401
            headers = {
                "Authentication": f"bearer {api_token.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            
            # DATOS DEL CUPÓN
            payload = {
                "code": "SITASAFE10",
                "type": "percentage",
                "value": "10",
                "min_price": "0",
                "max_uses": 50
            }
            
            with st.spinner("Sincronizando con Tiendanube..."):
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 201:
                        st.balloons()
                        st.success("### ✅ ¡ÉXITO TOTAL!")
                        st.write("El cupón **SITASAFE10** ha sido creado en tu tienda.")
                        st.markdown(f"[Ver cupones en mi tienda](https://admin.tiendanube.com/admin/{user_id}/promotions/coupons/)")
                    elif response.status_code == 401:
                        st.error("❌ Error 401: Token Inválido o Expirado.")
                        st.write("Genera un nuevo token en la barra lateral.")
                    elif response.status_code == 422:
                        st.warning("⚠️ El cupón 'SITASAFE10' ya existe en tu tienda.")
                    else:
                        st.error(f"Error {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"Ocurrió un error de conexión: {e}")

with col2:
    st.markdown("### 📈 Impacto Estimado")
    st.metric("Recuperación de Ventas", "+15.4%", "↑ 2.1%")
    st.metric("Tasa de Conversión", "3.2%", "↑ 0.5%")
    
    st.markdown("---")
    st.write("**Historial de Acciones:**")
    st.caption("- Creación de cupón 'SITASAFE10' (Pendiente)")
    st.caption("- Ajuste de SEO en categoría 'Chalecos' (Completado)")

st.markdown("---")
st.caption("NubePilot AI | Hackathon 2026 | Powered by Tiendanube API")
