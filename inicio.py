import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NubePilot AI - Hackathon", page_icon="🚀", layout="wide")

# --- BARRA LATERAL (EL DISEÑO QUE TE GUSTA) ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Autenticación API", expanded=True):
        st.info("Conexión Segura con Tiendanube")
        # Mostramos un token ficticio profesional
        st.code("shpat_live_942_sitasafetoken_2026")
        st.success("Access Token Validado ✅")

    st.write("---")
    st.text_input("Access Token de API", type="password", value="token_seguro_activado")
    st.text_input("ID de Tienda", value="2831942")
    
    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado a: **Sitasafe Store**")

# --- CUERPO PRINCIPAL (DISEÑO DINÁMICO) ---
st.markdown("# 🚀 NubePilot AI")
st.subheader("Tu Estratega de Crecimiento con IA para Tiendanube")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Mensaje de la IA
    with st.chat_message("assistant"):
        st.markdown("**IA NubePilot:** Hola William, he analizado Sitasafe. Detecté **12 carritos abandonados** en la última hora. El cupón **SITASAFE10** recuperaría el 22% de estas ventas. ¿Deseas activarlo?")
    
    st.write("")
    if st.button("🎯 Activar Estrategia de Recuperación"):
        with st.status("Sincronizando con Tiendanube API...", expanded=True) as status:
            st.write("Verificando credenciales de NubePilot...")
            time.sleep(1)
            st.write("Inyectando cupón SITASAFE10 vía REST API...")
            time.sleep(1)
            status.update(label="¡Sincronización Exitosa!", state="complete", expanded=False)
        
        st.balloons()
        st.success("### ✅ ¡CUPÓN 'SITASAFE10' CREADO EXITOSAMENTE!")
        st.info("Estrategia activa: El cupón ya está disponible para tus clientes en Sitasafe.")

with col_right:
    st.markdown("### 📊 Métricas de Impacto")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Tasa de Conversión", "3.5%", "+0.8%")
    
    st.divider()
    st.markdown("#### **Equipo 10:**")
    st.markdown("👤 **William L.** (Lead Architect)")
    st.markdown("👤 **Dalia** (Product Manager)")
    st.markdown("👤 **Montse** (Strategy)")

st.write("---")
st.caption("NubePilot AI | Hackathon UTEL 2026 - Presentación Final")
