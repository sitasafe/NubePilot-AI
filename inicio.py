import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- BARRA LATERAL (DISEÑO PROFESIONAL) ---
with st.sidebar:
    st.markdown("# ⚙️ Panel de Control")
    st.write("---")
    
    with st.expander("🔑 Autenticación API", expanded=True):
        st.info("Conexión Segura con Tiendanube")
        # Token simulado para el Pitch
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.write("---")
    st.text_input("Access Token de API", type="password", value="token_seguro_activado")
    st.text_input("ID de Tienda", value="2831942")
    
    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado a: **Sitasafe Store**")

# --- CUERPO PRINCIPAL (IDENTIDAD OFICIAL) ---
st.markdown("# 🚀 AI Growth Copilot")
st.subheader("Tu estratega de crecimiento con IA")
st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Mensaje de la IA con el nuevo nombre
    with st.chat_message("assistant"):
        st.markdown("**AI Growth Copilot:** Hola William, he analizado los datos de Sitasafe. Detecté **12 carritos abandonados** en la última hora. El cupón **SITASAFE10** recuperaría el 22% de estas ventas potenciales. ¿Deseas activarlo ahora?")
    
    st.write("")
    if st.button("🎯 Activar Estrategia de Recuperación"):
        with st.status("Sincronizando con Tiendanube API...", expanded=True) as status:
            st.write("Analizando métricas de conversión...")
            time.sleep(1)
            st.write("Inyectando cupón SITASAFE10 en la base de datos de Sitasafe...")
            time.sleep(1)
            status.update(label="¡Sincronización Exitosa!", state="complete", expanded=False)
        
        st.balloons()
        st.success("### ✅ ¡CUPÓN 'SITASAFE10' CREADO EXITOSAMENTE!")
        st.info("Estrategia activa: El Copilot ha configurado el descuento para tus clientes.")

with col_right:
    st.markdown("### 📊 Métricas de Impacto")
    st.metric("Ventas Recuperables", "$450.00", "+12%")
    st.metric("Tasa de Conversión", "3.5%", "+0.8%")
