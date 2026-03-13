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

# --- 3. DICCIONARIO MULTILINGÜE ---
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
        "sim_dias": "días",
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

# --- 7. ESTILOS CON EFECTOS ESPECIALES ---
bg_overlay = "rgba(255, 255, 255, 0.7)" if not alto_contraste else "rgba(0, 0, 0, 0.9)"
text_color = "#1E1E1E" if not alto_contraste else "#000000"

st.markdown(f"""
<style>
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes clouds-up {{
        0% {{ transform: translateY(100vh); opacity: 0; }}
        20% {{ opacity: 0.8; }}
        80% {{ opacity: 0.6; }}
        100% {{ transform: translateY(-100vh); opacity: 0; }}
    }}

    .cloud-effect {{
        position: fixed;
        font-size: 50px;
        z-index: 9999;
        pointer-events: none;
        animation: clouds-up 4s ease-in forwards;
    }}

    .stApp {{
        background: linear-gradient({bg_overlay}, {bg_overlay}), 
                    url("https://imgur.com/gQ7yynl.jpeg");
        background-attachment: fixed;
        background-size: cover;
    }}

    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        font-weight: 800;
        animation: gradient-move 3s linear infinite;
        margin-bottom: 0px;
    }}
    
    div[data-testid="stMetric"], .stTable, .team-card-large, div[data-testid="stExpander"] {{
        background-color: white !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 20px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }}

    div[data-testid="stMetric"]:hover, .stTable:hover, .team-card-large:hover {{
        transform: translateY(-5px) scale(1.01) !important;
        box-shadow: 0 12px 30px rgba(0,86,255,0.15) !important;
    }}

    div[data-testid="stTabs"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1) !important;
        border: none !important;
    }}

    div.stButton > button {{
        background: linear-gradient(90deg, #0056ff, #00c6ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        transition: 0.3s !important;
    }}
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

c_enc1, c_enc2 = st.columns([0.8, 0.2])
with c_enc1: 
    st.markdown(f"<div style='background:white; padding:10px 20px; border-radius:10px; display:inline-block; color:{text_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;'><strong>✨ {t_act['sub']}</strong></div>", unsafe_allow_html=True)

with c_enc2: 
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')
    if audio_data:
        st.toast(t_act["escuchando"])
        time.sleep(1)
        st.info(f"{t_act['voz_ok']} 'Optimizar inventario'")

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[0]:
    st.markdown(f"## {t_act['diferencia']}")
    col_v1, col_v2 = st.columns([0.6, 0.4])
    with col_v1:
        st.write(t_act["dolor"])
        st.info(t_act["dato_cert"])
    with col_v2:
        st.markdown(t_act["modelo_t"])
        st.write(f"{t_act['starter']}\n{t_act['growth']}\n{t_act['scale']}")

with tabs[1]:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")
    st.area_chart(df.set_index("Producto")["Stock"])

with tabs[2]:
    st.subheader(t_act["est_tit"])
    with st.expander(t_act["sim_tit"], expanded=True):
        sim_inv = st.number_input(t_act["sim_inv"], value=50000)
        c_s1, c_s2 = st.columns(2)
        with c_s1: st.markdown(f'<div style="background: linear-gradient(135deg, #0056ff 0%, #6200ea 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.15);"><small>{t_act["sim_proj"]}</small><h3>${sim_inv * (f_demanda * 1.8):,.0f} MXN</h3></div>', unsafe_allow_html=True)
        with c_s2: st.markdown(f'<div style="background: linear-gradient(135deg, #00c6ff 0%, #0056ff 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.15);"><small>{t_act["sim_rec"]}</small><h3>{30/f_demanda:.1f} {t_act["sim_dias"]}</h3></div>', unsafe_allow_html=True)
    
    st.write("---")
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"
    df["Accion"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Accion"]])
    
    def animar_nubes():
        cloud_placeholder = st.empty()
        cloud_placeholder.markdown("""
            <div class="cloud-effect" style="left: 10%; animation-delay: 0s;">☁️</div>
            <div class="cloud-effect" style="left: 30%; animation-delay: 0.5s;">☁️</div>
            <div class="cloud-effect" style="left: 55%; animation-delay: 0.2s;">☁️</div>
            <div class="cloud-effect" style="left: 80%; animation-delay: 0.8s;">☁️</div>
            <div class="cloud-effect" style="left: 45%; animation-delay: 1.2s;">☁️</div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button(t_act["btn_app"], use_container_width=True):
            animar_nubes()
            st.success(t_act["sync_ok"])
    
    with col_b2:
        csv = df.to_csv(index=False).encode('utf-8')
        if st.download_button(label=t_act["btn_reporte"], data=csv, file_name='Reporte_Flowmerce.csv', mime='text/csv', use_container_width=True):
            animar_nubes()
            st.toast(t_act["rep_exito"])

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"), # Foto actualizada
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos Andrés A.", "Liderazgo", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis Elizabeth", "Gestión", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("Cesar Augusto F.", "Estrategia", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    for i in range(0, len(equipo), 4):
        cols = st.columns(4)
        for j, (nombre, cargo, img) in enumerate(equipo[i:i+4]):
            with cols[j]:
                st.markdown(f"""<div class="team-card-large">
                    <img src="{img}" style="width: 110px; height: 110px; border-radius: 50%; object-fit: cover; margin-bottom: 10px;">
                    <br><strong>{nombre}</strong><br><small style="color:#0056ff;">{cargo}</small>
                </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")

