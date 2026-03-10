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
        background: linear-gradient(90deg, #0056ff 0%, #00c6ff 100%) !important;
        color: white !important; 
        border-radius: 25px !important; 
        border: none !important; 
        padding: 12px 30px !important;
        font-weight: bold !important; 
        transition: all 0.3s ease !important; 
        width: 100% !important; 
        font-size: 18px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 8px 20px rgba(0, 86, 255, 0.3) !important;
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
    
    /* Tarjetas de Equipo */
    .team-card {
        text-align: center; padding: 15px; border-radius: 15px;
        background: white; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); 
        margin-bottom: 20px; min-height: 180px;
    }
    .team-img { width: 50px !important; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Panel de Control) ---
with st.sidebar:
    st.image("https://logowik.com/content/uploads/images/tiendanube1485.logowik.com.webp", use_container_width=True)
    st.write("---")
    
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("## ⚙️ Panel de Control")
    
    with st.expander("🔑 Generador de Access Token", expanded=True):
        temp_code = st.text_input("Pega el 'Code' de Partners aquí")
        if st.button("Generar Token"):
            if temp_code:
                st.success("¡Token Creado!")
                st.code("shpat_6f8b9e2d4c1a5b0z9y8x7w6v5u4t3s2r1")
                st.info("⬆️ COPIA este código y pégalo abajo")
            else:
                st.warning("Escribe el código primero.")

    st.divider()
    
    api_token = st.text_input("Access Token de API", type="password", help="Pega el token generado arriba")
    id_tienda = st.text_input("ID de Tienda", value="2831942")
    
    if api_token:
        st.success("Estado: Conectado ✅")
    else:
        st.warning("Estado: Desconectado ⚠️")

# --- CUERPO PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 AI Growth</h1>', unsafe_allow_html=True)
st.subheader("Optimización  en Tiempo Real")
st.write("---")

tab_dash, tab_ins, tab_team = st.tabs(["📊 Dashboard General", "🧠 Insights Avanzados", "👥 Equipo"])

# --- TAB 1: DASHBOARD GENERAL ---
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
            st.write("🤖 **IA:** Hola Jiriam, detecté un aumento en carritos abandonados. ¿Activamos el cupón **SITASAFE10** para recuperar esas ventas?")
        
        if st.button("🎯 Activar Estrategia de Recuperación"):
            with st.status("Conectando con la API de Tiendanube...", expanded=True) as status:
                time.sleep(1.2)
                status.update(label="Generando cupón inteligente en la tienda...", state="running")
                time.sleep(1.2)
                status.update(label="¡Estrategia Desplegada!", state="complete", expanded=False)
            
            st.balloons()
            st.success("### 🚀 Estrategia de Recuperación Desplegada: Cupón SITASAFE10 activado.")

    with col_right:
        st.markdown("### 💬 Asesor Inteligente")
        u_input = st.text_input("Consulta a la IA:", placeholder="¿Cómo mejorar ventas?")
        if st.button("Enviar"):
            st.info(f"📊 **IA:** Analizando tendencias... Recomiendo activar envíos gratis en compras mayores a $999 para reducir el abandono en el checkout.")

# --- TAB 2: INSIGHTS AVANZADOS (Fusión con Review Intelligence) ---
with tab_ins:
    st.markdown("### 🧠 Review Intelligence: De Opiniones a Estrategia")
    st.caption("Nuestra IA analiza el sentimiento del mercado y las reseñas de la competencia para priorizar tu crecimiento.")
    
    col_ins1, col_ins2 = st.columns([1, 1])

    with col_ins1:
        st.markdown("#### 🚩 Hoja de Ruta Estratégica (Priorizada)")
        st.error("🚨 **URGENTE:** El 42% menciona 'dificultad de armado'. Recomendación: Crear video tutorial.")
        st.warning("⚠️ **OPORTUNIDAD:** Clientes piden empaques sustentables. Tu competencia ya lo ofrece.")
        st.info("💡 **INSIGHT:** Hay dudas recurrentes sobre impermeabilidad. Actualizar descripción hoy.")

    with col_ins2:
        st.markdown("#### 📊 Sentimiento del Mercado")
        data_sentimiento = pd.DataFrame({
            "Categoría": ["Calidad", "Envío", "Atención", "Precio"],
            "Tu Tienda": [85, 70, 90, 65],
            "Competencia": [80, 85, 75, 70]
        }).set_index("Categoría")
        st.bar_chart(data_sentimiento)

    st.divider()

    st.markdown("#### 🛒 Análisis de Productos con más Abandonos")
    df_abandonos = pd.DataFrame({
        "Producto": ["Playera Algodón", "Gorra Trucker", "Tenis Sport", "Sudadera Minimal"],
        "Abandonos": [45, 28, 15, 12],
        "Valor Perdido (MXN)": [13500, 7000, 18000, 9600],
        "Impacto": ["Crítico", "Medio", "Alto", "Bajo"]
    })

    col_table, col_chart = st.columns([2, 1])
    
    with col_table:
        st.dataframe(df_abandonos, use_container_width=True, hide_index=True)
    
    with col_chart:
        st.markdown("**Fuga de Capital Est.**")
        st.bar_chart(df_abandonos.set_index("Producto")["Valor Perdido (MXN)"])

    st.divider()
    st.markdown("#### 📈 Proyección de Recuperación con IA")
    st.line_chart(pd.DataFrame({"Ventas Proyectadas": [10, 25, 20, 50, 65, 90, 115]}))

# --- TAB 3: EQUIPO ---
with tab_team:
    st.markdown("### 👥 Equipo 3 - Desarrollo y Estrategia")
    
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://cdn-icons-png.flaticon.com/512/6840/6840478.png"),
        ("Dalia R.", "Product Manager", "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://cdn-icons-png.flaticon.com/512/4333/4333609.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png"),
        ("Edwing Garcia", "Ventas", "https://cdn-icons-png.flaticon.com/512/9431/9431149.png"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png")
    ]
    
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, icono) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""
                <div class="team-card">
                    <img src="{icono}" class="team-img"><br>
                    <strong>{nombre}</strong><br>
                    <small style="color: #666;">{cargo}</small>
                </div>
                """, unsafe_allow_html=True)

st.write("---")
st.caption("AI Growth | Equipo 3 | Hackathon UTEL 2026 | TiendaNube")

