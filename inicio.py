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
    # 1. LOGO DE TIENDANUBE (Alianza Estratégica)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Tiendanube_logo.svg/2560px-Tiendanube_logo.svg.png", width=180)
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

    # --- 3. CHAT INTERACTIVO MEJORADO (Factor Humano) ---
    st.write("---")
    st.markdown("### 💬 Asesor Inteligente")
    
    # Mensaje sugerido si no hay entrada
    prompt_placeholder = "Ej: ¿Qué producto debería promocionar hoy?"
    
    with st.container():
        user_input = st.text_input("Consulta a la IA sobre tu negocio:", placeholder=prompt_placeholder)
        enviar = st.button("Enviar Consulta")

    if enviar or user_input:
        if user_input:
            with st.chat_message("assistant"):
                with st.spinner("Analizando tendencias de mercado..."):
                    time.sleep(1.2)
                    if "venta" in user_input.lower() or "promocion" in user_input.lower():
                        st.write("📊 **Análisis Generativo:** Basado en el stock actual de **Sitasafe**, recomiendo una promoción relámpago en 'Cámaras WiFi'. La competencia ha subido precios un 5% hoy, dándote una ventaja competitiva inmediata.")
                    else:
                        st.write("🔍 **Sugerencia del Copilot:** He detectado que el 'Kit de Primeros Auxilios' tiene muchas visitas pero pocas ventas. Recomiendo revisar las fotos del producto o añadir un video testimonial.")
        else:
            st.warning("Por favor, escribe una pregunta para que el Asesor pueda ayudarte.")

    # --- SECCIÓN DE PRODUCTOS ---
    st.write("---")
    st.markdown("### 📦 Análisis de Productos (Top Abandonados)")
    chart_data = pd.DataFrame({
        "Productos": ["Cámara WiFi", "Sensor Pro", "Primeros Auxilios", "Cerradura Smart"],
        "Vistos": [120, 95, 80, 45],
        "Abandonados": [42, 28, 15, 10]
    })
    st.bar_chart(chart_data.set_index("Productos"))

with col_right:
    st.markdown("### 📊 Métricas de Impacto")
    m1, m2 = st.columns(2)
    m1.metric("Ventas Recup.", "$450.00", "+12%")
    m2.metric("Conversión", "3.5%", "+0.8%")
    
    st.write("---")
    st.markdown("#### 🏷️ Inteligencia de Precios")
    st.info("Tu precio promedio está **3% por debajo** de la competencia.")
    
    # 2. SECCIÓN DE PRÓXIMOS PASOS (Escalabilidad)
    st.write("---")
    st.markdown("#### 🚀 Próximos Pasos")
    st.markdown(f"""
    <div class="next-steps">
        <strong>Roadmap 2026:</strong><br>
        • Integración con Google Trends para predicción de stock.<br>
        • Automatización de campañas en Meta Ads.<br>
        • IA de reconocimiento visual para catálogo.
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
            st.write("")

st.write("---")
st.caption("AI Growth Copilot | Powered by Tiendanube | Hackathon UTEL 2026")
