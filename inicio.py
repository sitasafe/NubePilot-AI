import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import importlib

# --- BLOQUE DE CONTROL DE RUTAS ---
path_root = os.path.abspath(os.path.dirname(__file__))
if path_root not in sys.path:
    sys.path.insert(0, path_root)

# --- BLOQUE DE CONEXIÓN Y CREACIÓN DE BASE DE DATOS ---
from app.core.database import engine, Base

def inicializar_db_tablas(_st):
    try:
        import app.core.models
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        _st.error(f"Error al cargar base de datos: {e}")

try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

from app.core.state import (
    guardar_token_seguro,
    inicializar_estado_app,
    obtener_token_ref_desde_db,
    obtener_ultima_tienda_vinculada,
)
from app.services.tiendanube import (
    extraer_inventario_desde_snapshot,
    normalizar_store_id,
    obtener_snapshot_tiendanube,
    obtener_token_real,
)
from app.services.notifications import disparar_alerta_critica

inicializar_db_tablas(st)

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <link rel="apple-touch-icon" href="https://imgur.com/YrVO3ZF.jpeg">
    </head>
""", unsafe_allow_html=True)

# --- 2. CREDENCIALES ---
CLIENT_ID = "27483"
try:
    CLIENT_SECRET = st.secrets["TIENDANUBE_CLIENT_SECRET"]
except (KeyError, FileNotFoundError):
    CLIENT_SECRET = os.getenv("TIENDANUBE_CLIENT_SECRET", "")

# --- 3. DICCIONARIO ---
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
        "equipo_tit": "👥 Nuestro Equipo",
        "rep_proceso": "Procesando Reporte...",
        "rep_exito": "¡Reporte listo para descargar! ✅",
        "escuchando": "🎙️ Analizando captura de voz...",
        "voz_ok": "✅ Comando recibido: ",
        "criticos_tit": "🔎 Productos Críticos "
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
        "dato_cert": "💡 **Dado:** Reduzimos uma tarde inteira de trabajo a apenas 5 minutos de certeza.",
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
        "voz_ok": "✅ Comando recebido: ",
        "criticos_tit": "🔎 Produtos Críticos"
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
        "escuchando": "🎙️ Analyzing voice capture...",
        "voz_ok": "✅ Command received: ",
        "criticos_tit": "🔎 Critical Products"
    }
}

# --- 4. FUNCIONES MODULARES ---
def calcular_motor_analisis(df, f_demanda):
    if "Ventas_7d" in df.columns:
        base_30 = (df["Ventas_30d"] / 30).replace(0, np.nan)
        ratio = (df["Ventas_7d"] / 7) / base_30
        df["Tendencia"] = ratio.fillna(1.0).clip(0.5, 2.0)
    else:
        df["Tendencia"] = 1.0
    df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda * df["Tendencia"]
    df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], np.inf)
    return df

def color_estado(val):
    if "REABASTECER" in val: return "background-color: #ffcccc; color: black;"
    if "LIQUIDAR" in val: return "background-color: #fff3cd; color: black;"
    return "background-color: #d4edda; color: black;"

def exportar_csv(df_export):
    return df_export.to_csv(index=False).encode("utf-8")

# --- 5. GESTIÓN DE ESTADO ---
inicializar_estado_app()
if not st.session_state.token_ref and not st.session_state.tn_store_id:
    try:
        db_store_id, db_token_ref = obtener_ultima_tienda_vinculada()
        if db_store_id and db_token_ref:
            st.session_state.tn_store_id = db_store_id
            st.session_state.token_ref = db_token_ref
    except Exception:
        pass

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
        st.session_state.tn_store_id = st.text_input("3. Store ID (opcional)", value=st.session_state.tn_store_id)
        if st.button("3. Vincular Tienda"):
            token_data = obtener_token_real(temp_code, CLIENT_ID, CLIENT_SECRET)
            if token_data and token_data.get("access_token"):
                store_id_detectado = token_data.get("store_id") or st.session_state.tn_store_id
                st.session_state.token_ref = guardar_token_seguro(store_id_detectado, token_data["access_token"])
                st.session_state.tn_store_id = store_id_detectado
                st.success("✅ Tienda vinculada")
            else:
                st.info("Modo Demo ✅")
        if st.button("4. Sincronizar ahora", use_container_width=True):
            store_id = normalizar_store_id(st.session_state.tn_store_id)
            if store_id:
                st.session_state.tn_snapshot = obtener_snapshot_tiendanube(store_id, st.session_state.token_ref, CLIENT_ID)
                st.success("Snapshot actualizado")

# --- 7. ESTILOS ---
bg_overlay = "rgba(255, 255, 255, 0.7)" if not alto_contraste else "rgba(0, 0, 0, 0.9)"
text_color = "#1E1E1E" if not alto_contraste else "#FFFFFF"
st.markdown(f"""
<style>
    @keyframes gradient-move {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    .stApp {{ background: linear-gradient({bg_overlay}, {bg_overlay}), url("https://imgur.com/gQ7yynl.jpeg"); background-attachment: fixed; background-size: cover; }}
    .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem !important; font-weight: 800; animation: gradient-move 3s linear infinite; }}
    div[data-testid="stMetric"], .stTable, .team-card-large, div[data-testid="stExpander"] {{ background-color: white !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important; }}
    div[data-testid="stTabs"] {{ background-color: rgba(255, 255, 255, 0.95) !important; padding: 30px !important; border-radius: 20px !important; }}
</style>
""", unsafe_allow_html=True)

# --- 8. EJECUCIÓN MOTOR ---
t_act = textos[idioma]
snap = st.session_state.tn_snapshot
df_source = extraer_inventario_desde_snapshot(snap) if (snap and snap.get("ok")) else st.session_state.db_inventario.copy()
df = calcular_motor_analisis(df_source, f_demanda)
autonomia_finita = np.isfinite(df["Autonomia"])
atrapado_val = (df.loc[(df["Autonomia"] > 60) & autonomia_finita, "Stock"] * df.loc[(df["Autonomia"] > 60) & autonomia_finita, "Costo"]).sum()
riesgo_val = (df.loc[(df["Autonomia"] < dias_entrega) & autonomia_finita, "V_Diaria"] * df.loc[(df["Autonomia"] < dias_entrega) & autonomia_finita, "Costo"] * 1.5).sum()
salud_neta = min(100, max(0, 100 - int(riesgo_val / 1000)))

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown(f"<div style='background:white; padding:10px 20px; border-radius:10px; display:inline-block; color:{text_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;'><strong>✨ {t_act['sub']}</strong></div>", unsafe_allow_html=True)

if MIC_AVAILABLE:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')
    if audio_data: st.toast(t_act["escuchando"])

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[0]:
    st.markdown(f"## {t_act['diferencia']}")
    c1, c2 = st.columns([0.6, 0.4])
    c1.write(t_act["dolor"])
    c1.info(t_act["dato_cert"])
    c2.markdown(t_act["modelo_t"])
    c2.write(f"{t_act['starter']}\n{t_act['growth']}\n{t_act['scale']}")

with tabs[1]:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{salud_neta}%")
    st.progress(salud_neta / 100.0)
    st.bar_chart(df.set_index("Producto")["Autonomia"].replace(np.inf, 90))

with tabs[2]:
    st.subheader(t_act["est_tit"])
    with st.expander(t_act["sim_tit"], expanded=True):
        sim_inv = st.number_input(t_act["sim_inv"], value=50000)
        cs1, cs2 = st.columns(2)
        cs1.metric(t_act["sim_proj"], f"${sim_inv * (f_demanda * 1.8):,.0f} MXN")
        cs2.metric(t_act["sim_rec"], f"{30/f_demanda:.1f} {t_act['sim_dias']}")
    condiciones = [df["Autonomia"] < dias_entrega, df["Autonomia"] > 60]
    df["Accion"] = np.select(condiciones, ["🚨 REABASTECER", "🔥 LIQUIDAR"], default="✅ ESTABLE")
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Accion"]].style.map(color_estado, subset=["Accion"]), use_container_width=True)
    
    # --- BLOQUE CORREGIDO DE ALERTAS ---
    if st.button("🔔 Activar Monitor de Alertas Críticas", use_container_width=True):
        en_riesgo = df[df["Accion"] == "🚨 REABASTECER"]
        if not en_riesgo.empty:
            ok, msg = disparar_alerta_critica(en_riesgo)
            if ok:
                st.error(msg)
            else:
                st.info("Sin alertas pendientes")
        else:
            st.info("Todo estable")
    # -----------------------------------

    colb1, colb2 = st.columns(2)
    with colb1:
        if st.button(t_act["btn_app"], use_container_width=True): st.success(t_act["sync_ok"])
    with colb2:
        st.download_button(t_act["btn_reporte"], exportar_csv(df), "Reporte.csv", use_container_width=True)

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"), 
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
                card_html = f"""
                <div class="team-card-large" style="text-align:center; height: 220px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <img src="{img}" style="width:100px; height:100px; border-radius:50%; object-fit:cover; margin-bottom:10px;">
                    <div style="font-weight: bold; font-size: 1rem;">{nombre}</div>
                    <div style="font-size: 0.85rem; color: gray;">{cargo}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3 | TiendaNube")