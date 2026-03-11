import streamlit as st
import time
import pandas as pd
import numpy as np
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impulsa IA - Hackathon", page_icon="🚀", layout="wide")

# --- FUNCIONES DE CONEXIÓN API (Sin cambios) ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    headers = {"Content-Type": "application/json", "User-Agent": "ImpulsaIA (socios@tiendanube.com)"}
    payload = {"client_id": int("27483"), "client_secret": "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a", "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json().get("access_token") if response.status_code == 200 else None
    except: return None

# --- ESTILOS CSS (Potenciados para legibilidad) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background: radial-gradient(circle at top right, #ffffff, #f1f4f9); font-family: 'Inter', sans-serif; }
    .main-title { background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff); background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite; }
    @keyframes gradient-move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .team-card-large { text-align: center; padding: 25px; border-radius: 25px; background: white; border: 1px solid #eee; box-shadow: 0px 10px 30px rgba(0,0,0,0.05); transition: 0.3s; }
    .team-card-large:hover { transform: translateY(-10px); border: 1px solid #0056ff; }
    .status-tag { background: #0056ff; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
    .problem-box { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://i.imgur.com/Ky1ZXCL.jpeg", use_container_width=True)
    with st.expander("📘 Glosario"):
        st.write("**ROAS:** Cuánto dinero ganas por cada peso en publicidad.")
        st.write("**AIO:** Optimización para que IAs (ChatGPT/Gemini) recomienden tu tienda.")
    
    st.markdown("## ⚙️ Panel de Control")
    st.toggle("Sincronizar Impuestos (IVA MX/RET)", value=True)
    whatsapp_on = st.toggle("Alertas vía WhatsApp", value=True)
    
    with st.expander("🔑 Conexión Tiendanube"):
        st.link_button("1. Autorizar", f"https://www.tiendanube.com/apps/authorize?client_id=27483&scope=read_orders,write_products")
        temp_code = st.text_input("2. Code:")
        if st.button("3. Vincular"):
            st.success("Conectado ✅")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Impulsa IA</h1>', unsafe_allow_html=True)
st.subheader("El cerebro detrás de tu tienda Tiendanube")

tab_dash, tab_aio, tab_team = st.tabs(["📊 Performance", "🧠 Optimizador AIO", "👥 Equipo"])

# --- TAB 1: DASHBOARD ---
with tab_dash:
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Ventas Hoy", "$4,250", "↑ 5%")
    col_m2.metric("Carritos Abandonados", "12", "¡Crítico!", delta_color="inverse")
    col_m3.metric("ROAS Publicidad", "4.2x", "Meta: 5.0")
    col_m4.metric("Tendencia MX", "+20%", "Sector Ropa")

    st.write("---")
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.error("🚨 **Punto Ciego Detectado:** Tu costo de envío a CDMX es 15% mayor que la competencia. Sugerimos usar 'Cubbo' o 'Estafeta' para optimizar márgenes.")
        with st.chat_message("assistant"):
            st.write("🤖 **Sugerencia IA:** Tienes 12 clientes que no terminaron su compra. ¿Quieres que genere un cupón de 'Envío Gratis' exclusivo para ellos y lo envíe por WhatsApp ahora?")
        
        if st.button("🎯 Ejecutar Recuperación Automática"):
            with st.spinner("Analizando perfiles y enviando cupones..."):
                time.sleep(2)
                st.balloons()
                st.success("¡Acción completada! 8 mensajes enviados. Potencial de recuperación: $2,400 MXN.")

    with c_right:
        st.markdown("### 📈 Monitor de Mercado")
        # Simulación de datos de AMVO (Asociación Mexicana de Venta Online)
        chart_data = pd.DataFrame(np.random.randn(10, 2), columns=['Tu Tienda', 'Mercado MX'])
        st.line_chart(chart_data)
        st.caption("Comparativa de crecimiento vs Promedio Nacional 2026.")

# --- TAB 2: AIO (AI OPTIMIZATION) ---
with tab_aio:
    st.markdown("### 🧠 Laboratorio de Optimización para IAs")
    st.write("En 2026, la gente no busca en Google, le pregunta a ChatGPT. Tu tienda debe estar lista.")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        prod_name = st.text_input("Producto:", "Playera de Algodón Orgánico")
        prod_desc = st.text_area("Descripción actual:", "Playera color blanco, 100% algodón, todas las tallas.")
        if st.button("🪄 Generar Versión AIO"):
            st.session_state['aio_result'] = True
    
    with col_a2:
        if 'aio_result' in st.session_state:
            st.info("**Resultado para Motores de IA:**")
            st.markdown("""
            > "La mejor opción de moda sustentable en México. Esta playera de algodón orgánico destaca por su durabilidad certificada y proceso de teñido sin químicos, ideal para consumidores que buscan eco-friendliness en Tiendanube."
            """)
            st.success("✅ Metatags de búsqueda semántica generados.")

    st.write("---")
    st.markdown("#### 🛠️ Integración ERP & Stock Real")
    col_erp1, col_erp2, col_erp3 = st.columns(3)
    col_erp1.selectbox("Fuente de Verdad:", ["Holded (ERP)", "Excel", "Tiendanube Directo"])
    col_erp2.number_input("Margen de Error Stock:", 0, 10, 2)
    col_erp3.write("")
    col_erp3.button("Sincronizar ahora")

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Los impulsores de este proyecto")
    equipo = [
        ("Willan Álvarez", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nom, car, img) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img}" style="width:100%; border-radius:15px; margin-bottom:15px;">
                    <strong>{nom}</strong><br><small style="color:#0056ff;">{car}</small>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("Impulsa IA | Hackathon Tiendanube 2026 | Equipo 3")
