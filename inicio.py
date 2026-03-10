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
        color: white; border-radius: 25px; border: none; padding: 12px 30px;
        font-weight: bold; transition: all 0.3s ease; width: 100%; font-size: 18px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3);
    }

    /* Título con estilo moderno */
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800; margin-bottom: 0;
    }
    
    /* Cuadros de Review Intelligence (Basados en la imagen) */
    .review-card-urgent {
        background-color: #ffebee; padding: 15px; border-radius: 10px;
        border-left: 5px solid #ff4b4b; margin-bottom: 15px;
    }
    .review-card-advantage {
        background-color: #e8f5e9; padding: 15px; border-radius: 10px;
        border-left: 5px solid #4caf50; margin-bottom: 15px;
    }
    
    /* Tarjetas de Equipo */
    .team-card {
        text-align: center; padding: 15px; border-radius: 15px;
        background: white; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    .team-img { width: 45px !important; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control Restaurado) ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Conexión API Tiendanube", expanded=True):
        st.info("Estatus: Secure Link")
        st.markdown("**Store ID:** `sitasafe_6621` ")
        st.markdown("**Access Token:**")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Acceso Validado ✅")

    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado: **Sitasafe Store**")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("Tu estratega de crecimiento inteligente")
st.write("---")

# --- NAVEGACIÓN ---
tab_dash, tab_ins, tab_team = st.tabs(["📊 Dashboard General", "🧠 Insights Avanzados", "👥 Equipo"])

with tab_dash:
    st.markdown("### 📊 Estado Actual de la Tienda")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    m_col2.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    m_col3.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200")

    st.write("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        with st.chat_message("assistant"):
            st.write("🤖 **Ejecutando algoritmos de crecimiento...**")
            placeholder = st.empty()
            mensaje_ia = """**Análisis finalizado:** He detectado **12 carritos abandonados**. El cupón **GROWTH10** es la herramienta óptima con una probabilidad de éxito del 88%."""
            placeholder.markdown(mensaje_ia)
        
        if st.button("🎯 Activar Estrategia de Recuperación"):
            with st.status("Sincronizando con Tiendanube...", expanded=True) as status:
                time.sleep(1)
                st.write("Configurando descuentos dinámicos...")
                time.sleep(1)
                status.update(label="¡Estrategia Activa!", state="complete", expanded=False)
            st.balloons()
            st.success("### ✅ ¡CUPÓN 'GROWTH10' CREADO EXITOSAMENTE!")

    with col_right:
        st.markdown("### 💬 Asesor Inteligente")
        u_input = st.text_input("Consulta a la IA:", placeholder="¿Cómo mejorar ventas?")
        if st.button("Enviar"):
            if u_input:
                st.info(f"📊 **IA:** Para mejorar en '{u_input}', recomiendo optimizar stock hoy.")

with tab_ins:
    # SECCIÓN DE REVIEW INTELLIGENCE (NLP) AGREGADA
    st.markdown("### 🔍 Decodificador de Opiniones (NLP)")
    st.write("Análisis de sentimiento y benchmarking competitivo automático.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🚨 Acciones Urgentes")
        st.markdown("""<div class="review-card-urgent">
            <strong>⚠️ Dificultad de armado (42% de quejas)</strong><br>
            <small>➜ Acción: Crear video tutorial e incluirlo en el QR de envío.</small>
            </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="review-card-urgent">
            <strong>⚠️ Dudas de Impermeabilidad</strong><br>
            <small>➜ Acción: Actualizar FAQ y descripción del producto hoy mismo.</small>
            </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("#### 💡 Ventaja Competitiva")
        st.markdown("""<div class="review-card-advantage">
            <strong>✨ Calidad de Cremalleras (Mención Positiva)</strong><br>
            <small>➜ Acción: Resaltar este atributo en las campañas de Ads.</small>
            </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="review-card-advantage">
            <strong>✨ Eco-Packaging (Diferenciador)</strong><br>
            <small>➜ Acción: Añadir sello de sustentabilidad en la Home.</small>
            </div>""", unsafe_allow_html=True)
    
    st.write("---")
    c_ins_1, c_ins_2 = st.columns(2)
    with c_ins_1:
        st.markdown("#### 🛒 Productos con más Abandonos")
        df = pd.DataFrame({
            "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport"],
            "Abandonos": [8, 3, 1],
            "Pérdida": ["$800 MXN", "$450 MXN", "$250 MXN"]
        })
        st.table(df)
    with c_ins_2:
        st.markdown("#### 📈 Impacto Estimado")
        st.line_chart(pd.DataFrame({"Ventas": [10, 20, 15, 40, 50, 65, 80]}))

with tab_team:
    st.markdown("### 👥 Equipo 3 - Desarrollo y Estrategia")
    equipo = [
        ("Dalia Paola R.", "Capitana", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Willan Álvarez", "Lead Architect", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Montserrat G.", "Fotografía", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png"),
        ("Edwing Garcia", "Ventas", "https://cdn-icons-png.flaticon.com/512/9431/9431149.png"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png")
    ]
    
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, skill, icon) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card">
                    <img src="{icon}" class="team-img"><br>
                    <strong>{nombre}</strong><br>
                    <small>{skill}</small>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth Copilot | Equipo 3 | Hackathon UTEL 2026")
