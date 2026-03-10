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
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%);
        color: white; border-radius: 25px; border: none; padding: 12px 30px;
        font-weight: bold; transition: all 0.3s ease; width: 100%; font-size: 18px;
    }
    .main-title {
        background: -webkit-linear-gradient(#0056ff, #00c6ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800; margin-bottom: 0;
    }
    .review-card {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        border-left: 5px solid #ff4b4b; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .opportunity-card {
        background-color: #f0fff4; padding: 15px; border-radius: 10px;
        border-left: 5px solid #48bb78; margin-bottom: 10px;
    }
    .lead-card {
        background-color: #eef2ff; padding: 15px; border-radius: 10px;
        border: 1px solid #0056ff; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    st.markdown("## ⚙️ Panel de Control")
    with st.expander("🔑 Conexión API & Webhooks", expanded=False):
        st.info("Estatus: Tiendanube Secure Link")
        st.code("shpat_live_942_growth_copilot_2026")
        st.success("Webhooks WhatsApp Activos ✅")
    
    st.divider()
    st.markdown("### 📊 Estado de Tienda")
    st.success("Conectado: **Sitasafe Store**")
    st.warning("⚡ **Modo Demo:** Lógica basada en datos locales para optimizar consumo de tokens.")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth Copilot</h1>', unsafe_allow_html=True)
st.subheader("El cerebro inteligente para hacer crecer tu tienda")
st.write("---")

# --- NAVEGACIÓN POR PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📊 Growth Dashboard", "🧠 Review Intelligence", "🎯 Lead Scoring Predictivo"])

with tab1:
    # MÉTRICAS PRINCIPALES
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1: st.metric("Carritos Abandonados", "12", "↑ 2", delta_color="inverse")
    with m_col2: st.metric("Ventas del Mes", "$12,450 MXN", "↑ 12%")
    with m_col3: st.metric("Ventas Perdidas Est.", "$1,500 MXN", "-$200")

    st.write("---")
    c_left, c_right = st.columns([2, 1])

    with c_left:
        with st.chat_message("assistant"):
            st.write("🤖 **Ejecutando algoritmos de crecimiento...**")
            placeholder = st.empty()
            msg = "**Análisis finalizado:** He detectado 12 carritos abandonados. El cupón **GROWTH10** tiene una probabilidad de conversión del 88%. ¿Aplicamos?"
            placeholder.markdown(msg)
        
        if st.button("🎯 Activar Estrategia de Recuperación"):
            with st.status("Sincronizando...", expanded=False): time.sleep(1)
            st.balloons()
            st.success("### ✅ ¡CUPÓN 'GROWTH10' CREADO EN TIENDANUBE!")

        st.markdown("### 🛒 Productos Críticos")
        st.table(pd.DataFrame({"Producto": ["Playera", "Gorra", "Tenis"], "Abandonos": [8, 3, 1], "Pérdida": ["$800", "$450", "$250"]}))

    with c_right:
        st.markdown("### 📈 Impacto Estimado")
        st.line_chart(pd.DataFrame({"Semana": range(7), "Ventas": [10, 20, 15, 40, 50, 65, 80]}).set_index("Semana"))
        st.divider()
        st.markdown("#### 💬 Asesor IA")
        u_input = st.text_input("Consulta:", placeholder="¿Cómo subo ventas?")
        if u_input: st.info(f"📊 **IA:** Recomiendo optimizar stock de 'Cámaras WiFi' hoy.")

with tab2:
    st.markdown("### 🔍 Decodificador de Opiniones (NLP)")
    st.write("Análisis de sentimiento y benchmarking competitivo automático.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🚨 Acciones Urgentes")
        st.markdown('<div class="review-card"><strong>⚠️ Dificultad de armado (42%)</strong><br>➜ Acción: Crear video tutorial.</div>', unsafe_allow_html=True)
        st.markdown('<div class="review-card"><strong>⚠️ Impermeabilidad (Dudas)</strong><br>➜ Acción: Actualizar FAQ hoy.</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown("#### 💡 Ventaja Competitiva")
        st.markdown('<div class="opportunity-card"><strong>✨ Cremalleras Premium</strong><br>➜ Acción: Resaltar en Ads.</div>', unsafe_allow_html=True)
        st.markdown('<div class="opportunity-card"><strong>✨ Eco-Packaging</strong><br>➜ Acción: Añadir sello sustentable.</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 🎯 Lead Scoring Predictivo (WhatsApp + CRM)")
    st.write("Priorización inteligente de prospectos detectada vía Webhooks.")
    
    # SIMULACIÓN DE LEAD EN TIEMPO REAL
    st.markdown("""
    <div class="lead-card">
        <span style="background:#0056ff; color:white; padding:2px 8px; border-radius:5px;">NUEVO LEAD</span> 
        <strong> WhatsApp: +52 1 722... </strong><br>
        <i>"Quiero información del plan premium"</i><br>
        <hr>
        <strong>Análisis Predictivo:</strong><br>
        ✅ Intención: Alta Urgencia ("Quiero")<br>
        ✅ Historial: 60% cierre en leads similares<br>
        🔥 <strong>Score de Cierre: 85%</strong><br>
        <p style="color:#0056ff;">➜ Recomendación: Llamar de inmediato / Enviar oferta Premium.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📊 Embudo de Conversión IA")
    df_leads = pd.DataFrame({"Estado": ["Leads Fríos", "Interés Medio", "Alta Probabilidad (80%+)"], "Cantidad": [50, 20, 5]})
    st.bar_chart(df_leads.set_index("Estado"))

# --- EQUIPO ---
st.write("---")
with st.expander("👥 Equipo 3 - Desarrollo y Estrategia", expanded=True):
    equipo = [
        ("Dalia Paola", "Capitana"), ("Willan Álvarez", "Lead Architect"), 
        ("Montserrat G.", "Fotografía"), ("Jiram Cabrera", "Organización"),
        ("Cesar Augusto", "Estrategia"), ("Edwing Garcia", "Ventas"),
        ("Carlos Andrés", "Liderazgo"), ("Amarilis E.", "Gestión")
    ]
    cols = st.columns(4)
    for i, (n, r) in enumerate(equipo):
        cols[i % 4].markdown(f"**{n}**\n<small>{r}</small>", unsafe_allow_html=True)

st.caption("AI Growth Copilot | Hackathon UTEL 2026")
