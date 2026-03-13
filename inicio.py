import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# --- 2. CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- 3. DICCIONARIO MULTILINGÜE COMPLETO ---
textos = {
    "Español": {
        "sub": "Donde los datos se convierten en ventas",
        "tab0": "🚀 Nuestra Visión", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estrategia", "tab3": "👥 Equipo",
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja",
        "diferencia": "🎯 ¿Qué nos diferencia?",
        "dolor": "Hoy, miles de dueños de marcas pasan **5 horas por semana** frente a un Excel, intentando adivinar el futuro. Flowmerce transforma datos de ventas en decisiones automáticas.",
        "modelo_t": "### 💎 Modelo de Negocio (SaaS)",
        "starter": "- **Starter (Gratis):** Alertas básicas.",
        "growth": "- **Growth ($20 USD):** Predicción IA.",
        "scale": "- **Scale (Premium):** Simulador de escenarios.",
        "dato_cert": "💡 **Dato:** Reducimos una tarde entera de trabajo a solo 5 minutos de certeza.",
        "est_tit": "🧠 Estrategia e Inteligencia de Datos",
        "sim_tit": "💎 Simulador de Liquidez (Nivel Scale)",
        "sim_inv": "Inversión a Simular ($)",
        "sim_proj": "Ventas Proyectadas",
        "sim_rec": "Recuperación en",
        "sim_dias": "días",
        "btn_app": "🚀 Aplicar a Tiendanube",
        "btn_reporte": "📝 Generar Reporte y Descargar",
        "sync": "Sincronizando...",
        "sync_ok": "Sincronización Exitosa!",
        "equipo_tit": "👥 Equipo Multidisciplinario (Equipo 3)",
        "rep_proceso": "Procesando Reporte...",
        "rep_exito": "¡Reporte listo para descargar! ✅",
        "escuchando": "🎙️ Analizando comando de voz...",
        "voz_ok": "✅ Comando recibido: "
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas",
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa",
        "diferencia": "🎯 O que nos diferencia?",
        "dolor": "Hoje, milhares de donos de marcas passam **5 horas por semana** na frente de um Excel, tentando adivinhar o futuro. Flowmerce transforma datos de vendas em decisões automáticas.",
        "modelo_t": "### 💎 Modelo de Negócio (SaaS)",
        "starter": "- **Starter (Grátis):** Alertas básicos.",
        "growth": "- **Growth ($20 USD):** Predição IA.",
        "scale": "- **Scale (Premium):** Simulador de cenários.",
        "dato_cert": "💡 **Dado:** Reduzimos uma tarde inteira de trabalho a apenas 5 minutos de certeza.",
        "est_tit": "🧠 Estratégia e Inteligência de Datos",
        "sim_tit": "💎 Simulador de Liquidez (Nível Scale)",
        "sim_inv": "Investimento para Simular ($)",
        "sim_proj": "Vendas Projetadas",
        "sim_rec": "Recuperação em",
        "sim_dias": "dias",
        "btn_app": "🚀 Aplicar na Tiendanube",
        "btn_reporte": "📝 Gerar Relatório e Baixar",
        "sync": "Sincronizando...",
        "sync_ok": "Sincronização com Sucesso!",
        "equipo_tit": "👥 Equipe Multidisciplinar (Equipe 3)",
        "rep_proceso": "Processando Relatório...",
        "rep_exito": "Relatório pronto para baixar! ✅",
        "escuchando": "🎙️ Analisando comando de voz...",
        "voz_ok": "✅ Comando recebido: "
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Our Vision", "tab1": "📊 Liquidity Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health",
        "diferencia": "🎯 What makes us different?",
        "dolor": "Today, thousands of brand owners spend **5 hours per week** in front of an Excel, trying to guess the future. Flowmerce transforms sales data into automated decisions.",
        "modelo_t": "### 💎 Business Model (SaaS)",
        "starter": "- **Starter (Free):** Basic alerts.",
        "growth": "- **Growth ($20 USD):** AI Prediction.",
        "scale": "- **Scale (Premium):** Scenario simulator.",
        "dato_cert": "💡 **Fact:** We reduce an entire afternoon of work to just 5 minutes of certainty.",
        "est_tit": "🧠 Strategy and Data Intelligence",
        "sim_tit": "💎 Liquidity Simulator (Scale Level)",
        "sim_inv": "Investment to Simulate ($)",
        "sim_proj": "Projected Sales",
        "sim_rec": "Recovery in",
        "sim_dias": "days",
        "btn_app": "🚀 Apply to Tiendanube",
        "btn_reporte": "📝 Generate Report & Download",
        "sync": "Syncing...",
        "sync_ok": "Successful Synchronization!",
        "equipo_tit": "👥 Multidisciplinary Team (Team 3)",
        "rep_proceso": "Processing Report...",
        "rep_exito": "Report ready to download! ✅",
        "escuchando": "🎙️ Analyzing voice command...",
        "voz_ok": "✅ Command received: "
    }
}

# --- 4. FUNCIONES DE API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("access_token") if response.status_code == 200 else None
    except: return None

# --- 5. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })
if 'token_session' not in st.session_state:
    st.session_state.token_session = None

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.markdown("""
    <style>
        @keyframes float {
            0% { transform: translateY(0px); filter: drop-shadow(0 5px 15px rgba(0,86,255,0.2)); }
            50% { transform: translateY(-10px); filter: drop-shadow(0 25px 15px rgba(0,86,255,0.1)); }
            100% { transform: translateY(0px); filter: drop-shadow(0 5px 15px rgba(0,86,255,0.2)); }
        }
        .logo-flow { animation: float 4s ease-in-out infinite; border-radius: 20px; margin-bottom: 20px; }
    </style>
    <div style="text-align: center;">
        <img src="https://imgur.com/YrVO3ZF.jpeg" class="logo-flow" style="width: 100%;">
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    with st.expander("🌐 Accesibilidad e Idioma", expanded=True):
        idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_orders,read_products,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state.token_session = token
                st.success("✅")
            else:
                st.session_state.token_session = "demo"
                st.info("Modo Demo ✅")

# --- 7. LÓGICA DINÁMICA DE CSS ---
# Ajustamos overlay para que se vean mejor las caras del fondo (menos opacidad)
bg_overlay = "rgba(255, 255, 255, 0.4)" if not alto_contraste else "rgba(0, 0, 0, 0.85)"
card_bg = "rgba(255, 255, 255, 0.8)" if not alto_contraste else "#FFFFFF"
text_color = "#1E1E1E" if not alto_contraste else "#000000"
font_size = "1.2rem" if lectura_facil else "1rem"
title_size = "5rem" if lectura_facil else "4rem"

st.markdown(f"""
<style>
    html, body, [class*="st-"] {{
        font-size: {font_size} !important;
        { 'font-family: Arial, sans-serif !important;' if lectura_facil else '' }
    }}

    .stApp {{
        background: linear-gradient({bg_overlay}, {bg_overlay}), 
                    url("https://imgur.com/gQ7yynl.jpeg");
        background-attachment: fixed;
        background-size: cover;
    }}

    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: {title_size} !important; font-weight: 800; animation: gradient-move 4s ease infinite; 
    }}
    
    /* ELIMINACIÓN DE BORDES AZULES EN TARJETAS Y TABLAS */
    div[data-testid="stMetric"], .stTable, .team-card-large, .stTabs, div[data-testid="stExpander"] {{
        background-color: {card_bg} !important;
        backdrop-filter: blur(8px);
        border-radius: 15px !important;
        border: none !important; /* QUITAMOS EL BORDE AZUL */
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
        color: {text_color} !important;
    }}

    .stTable td, .stTable th, .stTable p {{
        color: {text_color} !important;
        border: none !important;
    }}

    div.stButton > button {{
        background: #0056ff !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }}

    .team-card-large strong {{ color: #0056ff !important; }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE CÁLCULO ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)
atrapado_val = (df[df["Autonomia"] > 60]["Stock"] * df[df["Autonomia"] > 60]["Costo"]).sum()
riesgo_val = (df[df["Autonomia"] < dias_entrega]["V_Diaria"] * df[df["Autonomia"] < dias_entrega]["Costo"] * 1.5).sum()

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

c_enc1, c_enc
