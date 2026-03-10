import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Botón con degradado dinámico */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 18px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3);
    }

    /* Título con estilo moderno */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    
    /* Estilo para los nombres del equipo */
    .member-name { font-weight: bold; font-size: 14px; margin-bottom: -5px; }
    .member-skill { color: #6c757d; font-size: 12px; font-style: italic; }
    
    /* Tarjeta de Próximos Pasos */
    .next-steps {
        background-color: #eef2ff;
        padding: 15px;
        border-left: 5px solid #0056ff;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # --- LOGO DE TIENDANUBE SUBIDO (image_4e641f.png) ---
    st.image("image_4e641f.png", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Conexión API", expanded=True):
        st.info("Estatus: Tiendanube Secure Link")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Tu estratega de crecimiento inteligente")
st.write("---")

# --- SECCIÓN: ESTADO ACTUAL DE LA TIENDA ---
st.markdown("### 📊 Estado Actual de la Tienda")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
with m_col2:
    st.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
with m_col3:
    st.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200")

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # --- MÓDULO DE IA GENERATIVA ---
    with st.chat_message("assistant"):
        st.write("🤖 **Ejecutando algoritmos de crecimiento...**")
        placeholder = st.empty()
        
        mensaje_ia = """**Análisis del Copilot finalizado:** He detectado una ventana de oportunidad en **12 carritos abandonados**. 

Tras procesar los patrones de demanda y la disponibilidad actual en el inventario, el sistema ha diseñado la siguiente estrategia de conversión:

El cupón **GROWTH10** es la herramienta óptima para incentivar el cierre de estas ventas con una probabilidad de éxito del 88%. ¿Deseas aplicar esta acción ahora?"""
        
        full_response = ""
        for char in mensaje_ia:
            full_response += char
            placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
        placeholder.markdown(full_response)
    
    st.write("")
    if st.button("🎯 Activar Estrategia de Recuperación"):
        with st.status("Sincronizando con Tiendanube...", expanded=True) as status:
            time.sleep(1)
            st.write("Configurando descuentos dinámicos...")
            time.sleep(1)
            status.update(label="¡Estrategia Activa!", state="complete", expanded=False)
        st.balloons()
        st.success("### ✅ ¡CUPÓN 'GROWTH10' CREADO EXITOSAMENTE EN TIENDANUBE!")

    # --- SECCIÓN: PRODUCTOS CON MÁS ABANDONOS ---
    st.write("---")
    st.markdown("### 🛒 Productos con más Abandonos")
    st.write("Detalle de productos que requieren atención inmediata:")
    df_productos = pd.DataFrame({
        "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
        "Abandonos": [8, 3, 1],
        "Perdida Est.": ["$800 MXN", "$450 MXN", "$250 MXN"]
    })
    st.table(df_productos)

    # --- SECCIÓN: IMPACTO ESTIMADO (Tendencia) ---
    st.write("---")
    st.markdown("### 📈 Impacto Estimado de NubePilot")
    st.write("Proyección de recuperación de ventas al aplicar las estrategias de la IA:")
    chart_data = pd.DataFrame({
        "Semana": [0, 1, 2, 3, 4, 5, 6],
        "Ventas ($)": [10, 20, 15, 40, 50, 65, 80]
    })
    st.line_chart(chart_data.set_index("Semana"))

with col_right:
    # --- CHAT INTERACTIVO ---
    st.markdown("### 💬 Asesor Inteligente")
    prompt_placeholder = "Ej: ¿Qué producto debería promocionar hoy?"
    user_input = st.text_input("Consulta a la IA sobre tu negocio:", placeholder=prompt_placeholder)
    enviar = st.button("Enviar Consulta")

    if enviar or user_input:
        if user_input:
            with st.chat_message("assistant"):
                with st.spinner("Analizando tendencias..."):
                    time.sleep(1.2)
                    st.write("📊 **Análisis Generativo:** Basado en el stock, recomiendo una promoción relámpago en 'Cámaras WiFi'. La competencia ha subido precios un 5% hoy.")
        else:
            st.warning("Escribe una pregunta para el Asesor.")
    
    st.write("---")
    st.markdown("#### 🚀 Próximos Pasos")
    st.markdown(f"""
    <div class="next-steps">
        <strong>Roadmap 2026:</strong><br>
        • Integración con Google Trends.<br>
        • Automatización de campañas Meta Ads.<br>
        • IA de reconocimiento visual.
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("#### 👥 Equipo 3")
    
    equipo = [
        ("Dalia Paola Rodríguez Trejo", "Capitana / Comunicación", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Willan Álvarez Carmona", "Lead Architect / AI Dev", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Montserrat Garcia Barona", "Fotografía / Redacción", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera Ramos", "Organización / Empatía", "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"),
        ("Cesar Augusto Fernandez Delgado", "Estrategia / Operaciones", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png"),
        ("Edwing Garcia Juarez", "Ventas / Publicidad", "https://cdn-icons-png.flaticon.com/512/9431/9431149.png"),
        ("Carlos Andrés Almeida Rangel", "Liderazgo / Organización", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Amarilis Elizabeth Vera García", "Gestión / Análisis", "https://cdn-icons-png.flaticon.com/512/201/201634.png")
    ]
    
    for nombre, skill, icon in equipo:
        c1, c2 = st.columns([1, 4])
        with c1:
            st.image(icon, width=35)
        with c2:
            st.markdown(f'<p class="member-name">{nombre}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="member-skill">{skill}</p>', unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | Powered by Tiendanube | Hackathon UTEL 2026")
