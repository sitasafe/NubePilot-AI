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
        "dolor": "Flowmerce transforma datos de ventas en decisiones automáticas.",
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
        "btn_app": "🚀 Vincular Tienda",
        "btn_reporte": "📝 Descargar Reporte Premium",
        "sync": "Sincronizando...",
        "sync_ok": "Sincronización Exitosa!",
        "equipo_tit": "👥 Equipo Multidisciplinario",
        "rep_proceso": "Procesando Reporte...",
        "rep_exito": "¡Reporte generado! ☁️"
    },
    "Português": { "sub": "Onde os dados se transformam em vendas", "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe", "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde", "diferencia": "🎯 Diferencial", "dolor": "Decisões automáticas.", "modelo_t": "### SaaS", "starter": "- Starter", "growth": "- Growth", "scale": "- Scale", "dato_cert": "5 minutos.", "est_tit": "Inteligência", "sim_tit": "Simulador", "sim_inv": "Investimento", "sim_proj": "Projeção", "sim_rec": "Recuperação", "sim_dias": "dias", "btn_app": "🚀 Vincular", "btn_reporte": "📝 Baixar Relatório", "sync": "Sinc...", "sync_ok": "Sucesso!", "equipo_tit": "Equipe", "rep_proceso": "Processando...", "rep_exito": "Pronto! ☁️" },
    "English": { "sub": "Data into sales", "tab0": "🚀 Vision", "tab1": "📊 Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team", "atrapado": "Trapped Capital", "riesgo": "Risk Sales", "salud": "Health", "diferencia": "🎯 Difference", "dolor": "Automatic decisions.", "modelo_t": "### SaaS", "starter": "- Starter", "growth": "- Growth", "scale": "- Scale", "dato_cert": "5 minutes.", "est_tit": "Intelligence", "sim_tit": "Simulator", "sim_inv": "Investment", "sim_proj": "Projection", "sim_rec": "Recovery", "sim_dias": "days", "btn_app": "🚀 Link Store", "btn_reporte": "📝 Download Report", "sync": "Sync...", "sync_ok": "Success!", "equipo_tit": "Team", "rep_proceso": "Processing...", "rep_exito": "Ready! ☁️" }
}

# --- 4. ESTILOS CSS AVANZADOS (3D y EFECTOS) ---
st.markdown(f"""
<style>
    /* Titulo con Gradiente Animado */
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite; 
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}

    /* Botones 3D Dinámicos */
    div.stButton > button, div.stDownloadButton > button {{
        background: linear-gradient(145deg, #0056ff, #0045cc) !important;
        color: white !important;
        border: none !important;
        padding: 15px 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 6px #003399, 0 10px 20px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px #003399, 0 12px 25px rgba(0,0,0,0.3) !important;
    }}
    div.stButton > button:active, div.stDownloadButton > button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 2px #003399 !important;
    }}

    /* Efectos en Tablas */
    table {{
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    tr:hover {{
        background-color: rgba(0, 86, 255, 0.05) !important;
        transition: 0.3s;
    }}

    /* Animación de Nubes */
    @keyframes cloud-fly {{
        0% {{ transform: translateY(100vh) translateX(0); opacity: 0; }}
        20% {{ opacity: 0.8; }}
        80% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-100vh) translateX(20px); opacity: 0; }}
    }}
    .cloud-effect {{
        position: fixed; bottom: -100px; font-size: 4rem; z-index: 9999;
        pointer-events: none; animation: cloud-fly 3s ease-in-out infinite;
    }}

    /* Cartas de Equipo 3D */
    .team-card-large {{
        text-align: center; padding: 25px; border-radius: 25px;
        background: white; border: 1px solid rgba(0, 86, 255, 0.1);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .team-card-large:hover {{
        transform: scale(1.05) rotateY(10deg);
        box-shadow: 0 20px 40px rgba(0, 86, 255, 0.15);
    }}
</style>
""", unsafe_allow_html=True)

# --- 5. LOGICA DE NUBES ---
def disparar_nubes():
    placeholders = [st.empty() for _ in range(5)]
    for i, p in enumerate(placeholders):
        left = 10 + (i * 20)
        p.markdown(f'<div class="cloud-effect" style="left:{left}%; animation-delay:{i*0.4}s;">☁️</div>', unsafe_allow_html=True)
    time.sleep(3)
    for p in placeholders: p.empty()

# --- 6. GESTIÓN DE DATOS ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })
if 'token_session' not in st.session_state: st.session_state.token_session = None

# --- 7. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
    idioma = st.selectbox("🌐 Idioma", ["Español", "Português", "English"])
    f_demanda = st.slider("📈 Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("🚚 Lead Time", 1, 30, 7)

# --- 8. CUERPO PRINCIPAL ---
t_act = textos[idioma]
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)
atrapado_val = (df[df["Autonomia"] > 60]["Stock"] * df[df["Autonomia"] > 60]["Costo"]).sum()
riesgo_val = (df[df["Autonomia"] < dias_entrega]["V_Diaria"] * df[df["Autonomia"] < dias_entrega]["Costo"] * 1.5).sum()

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[1]:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="⚠️")
    col3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")
    # Gráfico de Área con Estilo Pro
    st.area_chart(df.set_index("Producto")["Stock"], color="#0056ff")

with tabs[2]:
    st.subheader(t_act["est_tit"])
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"
    
    df["Accion"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Accion"]])
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button(t_act["btn_app"], use_container_width=True):
            with st.status(t_act["sync"]): time.sleep(1); st.success(t_act["sync_ok"])
    
    with col_b2:
        csv = df.to_csv(index=False).encode('utf-8')
        if st.download_button(
            label=t_act["btn_reporte"],
            data=csv,
            file_name=f'Flowmerce_Report_{int(time.time())}.csv',
            mime='text/csv',
            use_container_width=True
        ):
            disparar_nubes() # Lanza el efecto de nubes al hacer click
            st.balloons()

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    equipo = [
        ("Willan Álvarez", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg")
    ]
    cols = st.columns(4)
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i]:
            st.markdown(f"""<div class="team-card-large">
                <img src="{img}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #0056ff;">
                <br><b>{nombre}</b><br><small style="color:#0056ff;">{cargo}</small>
            </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
