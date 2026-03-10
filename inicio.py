import streamlit as st
import time
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AI Growth Copilot - Hackathon", page_icon="🚀", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (Mejorados) ---
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
    
    /* Tarjeta de Próximos Pasos (Más visual) */
    .next-steps {
        background-color: #ffffff;
        padding: 20px;
        border-left: 5px solid #00c6ff;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Estilo para métricas */
    [data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #0056ff; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Conexión API", expanded=False): # Cambiado a False para limpiar la vista inicial
        st.info("Estatus: Tiendanube Secure Link")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Access Token Validado ✅")

    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado: **Sitasafe Store**")
    st.info("💡 **Tip del día:** Las promociones con envío gratis aumentan 20% el cierre de carritos.")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Tu estratega de crecimiento inteligente para Tiendanube")
st.write("---")

# --- NAVEGACIÓN (NUEVO: Ayuda a organizar el contenido) ---
tab_dashboard, tab_insights = st.tabs(["📊 Dashboard General", "🧠 Insights Avanzados"])

with tab_dashboard:
    # --- SECCIÓN: ESTADO ACTUAL (Métricas con contenedores) ---
    st.markdown("### 📈 Rendimiento en Tiempo Real")
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

Tras procesar los patrones de demanda y el inventario, el sistema recomienda:

El cupón **GROWTH10** es la herramienta óptima para incentivar el cierre de estas ventas con una probabilidad de éxito del 88%."""
            
            full_response = ""
            for char in mensaje_ia:
                full_response += char
                placeholder.markdown(full_response + "▌")
                time.sleep(0.005) # Un poco más rápido para mejor experiencia
            placeholder.markdown(full_response)
        
        st.write("")
        if st.button("🎯 Activar Estrategia de Recuperación"):
            with st.status("Sincronizando con Tiendanube...", expanded=True) as status:
                time.sleep(1)
                st.write("Generando cupones dinámicos...")
                time.sleep(1)
                status.update(label="¡Estrategia Activa!", state="complete", expanded=False)
            st.balloons()
            st.success("### ✅ ¡CUPÓN 'GROWTH10' SINCRONIZADO!")

    with col_right:
        # --- CHAT INTERACTIVO ---
        st.markdown("### 💬 Asesor Inteligente")
        user_input = st.text_input("Consulta a la IA:", placeholder="¿Cómo mejorar ventas?")
        if st.button("Enviar"):
            if user_input:
                with st.chat_message("assistant"):
                    st.write(f"📊 **Análisis:** Para mejorar en '{user_input}', recomiendo optimizar stock en 'Cámaras WiFi' hoy.")
            else:
                st.warning("Escribe una consulta primero.")

with tab_insights:
    col_ins_1, col_ins_2 = st.columns(2)
    with col_ins_1:
        st.markdown("### 🛒 Productos Críticos")
        df_productos = pd.DataFrame({
            "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
            "Abandonos": [8, 3, 1],
            "Pérdida Est.": ["$800 MXN", "$450 MXN", "$250 MXN"]
        })
        st.table(df_productos)
    
    with col_ins_2:
        st.markdown("### 📈 Impacto Proyectado")
        chart_data = pd.DataFrame({
            "Semana": [0, 1, 2, 3, 4, 5, 6],
            "Ventas ($)": [10, 20, 15, 40, 50, 65, 80]
        })
        st.line_chart(chart_data.set_index("Semana"))

# --- PIE DE PÁGINA Y EQUIPO ---
st.write("---")
col_footer_1, col_footer_2 = st.columns([2, 1])

with col_footer_1:
    st.markdown("#### 👥 Equipo de Desarrollo 3")
    equipo = [
        ("Dalia Paola Rodríguez Trejo", "Capitana", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Willan Álvarez Carmona", "Lead Architect", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Montserrat Garcia Barona", "Fotografía", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera Ramos", "Organización", "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"),
        ("Cesar Augusto Fernandez Delgado", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png"),
        ("Edwing Garcia Juarez", "Ventas", "https://cdn-icons-png.flaticon.com/512/9431/9431149.png"),
        ("Carlos Andrés Almeida Rangel", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Amarilis Elizabeth Vera García", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png")
    ]
    
    # Mostrar equipo en cuadrícula de 2 columnas para no alargar tanto la página
    eq_col1, eq_col2 = st.columns(2)
    for i, (nombre, skill, icon) in enumerate(equipo):
        target_col = eq_col1 if i % 2 == 0 else eq_col2
        with target_col:
            st.markdown(f"![icon]({icon}) **{nombre}** \n *{skill}*", unsafe_allow_html=True)

with col_footer_2:
    st.markdown("#### 🚀 Futuro del Copilot")
    st.markdown("""<div class="next-steps">
        <strong>Roadmap 2026:</strong><br>
        • 📈 Integración Google Trends<br>
        • 📱 Notificaciones Push IA<br>
        • 🤖 Ads Automáticos con GenAI
        </div>""", unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | Powered by Tiendanube | Hackathon UTEL 2026")
