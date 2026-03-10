import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# DATOS DE IDENTIFICACIÓN
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- BARRA LATERAL (EL DISEÑO QUE TE GUSTA) ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Generador de Access Token", expanded=True):
        st.caption("Pega el 'Code' de Partners abajo")
        temp_code = st.text_input("Code", label_visibility="collapsed")
        
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
                    nuevo_token = res.json().get('access_token')
                    st.success("¡Token creado!")
                    st.code(nuevo_token)
                    st.info("⬆️ COPIA este código y pégalo abajo")
                else:
                    st.error("Error: Code inválido")
            else:
                st.warning("Escribe el código")

    st.write("---")
    # Este es el campo clave: Aquí debes pegar el token que generaste arriba
    api_token = st.text_input("Access Token de API", type="password", help="Pega el código que generaste arriba")
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token:
        st.success("Estado: Conectado ✅")
    else:
        st.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL (DISEÑO DINÁMICO) ---
st.markdown("# 🚀 NubePilot AI")
st.subheader("Optimización en Tiempo Real para Sitasafe")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Mensaje de la IA
    st.info("🤖 **IA:** Hola William, he detectado carritos abandonados. ¿Creamos el cupón **SITASAFE10** ahora?")
    
    if st.button("🎯 Activar Estrategia"):
        if not api_token:
            st.error("❌ Falta el Access Token en el panel lateral.")
        else:
            url = f"https://api.tiendanube.com/2025-03/{id_tienda}/coupons"
            headers = {
                "Authentication": f"bearer {api_token.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "NubePilot AI (willysitasafe@gmail.com)"
            }
            payload = {"code": "SITASAFE10", "type": "percentage", "value": "10", "max_uses": 50}
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 201:
                    st.balloons()
                    st.success("### ✅ ¡CUPÓN CREADO EXITOSAMENTE!")
                elif response.status_code == 422:
                    st.warning("⚠️ El cupón ya existe en tu tienda.")
                else:
                    st.error(f"Error {response.status_code}: Token inválido.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

with col_right:
    st.markdown("### 📊 Métricas Clave")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### **Equipo 10:**")
    st.markdown("👤 **William L.** (Lead Architect)")
    st.markdown("👤 **Dalia** (Product Manager)")
    st.markdown("👤 **Montse** (Strategy)")
    st.markdown("👤 **Integrantes Equipo 10**")

st.write("---")
st.caption("NubePilot AI | Hackathon UTEL 2026")
