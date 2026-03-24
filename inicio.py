import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import importlib

# --- 1. CONFIGURACIÓN DE PÁGINA (DEBE SER LO PRIMERO) ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# --- 2. BLINDAJE DE RUTAS PARA STREAMLIT CLOUD ---
path_root = os.path.abspath(os.path.dirname(__file__))
if path_root not in sys.path:
    sys.path.insert(0, path_root)

# --- 3. IMPORTACIONES DINÁMICAS ---
from app.core.database import engine, Base

def inicializar_db_tablas(_st):
    try:
        # Importación forzada para que SQLAlchemy encuentre los modelos
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

# Ejecutar inicialización
inicializar_db_tablas(st)
inicializar_estado_app()

# --- 4. CREDENCIALES ---
CLIENT_ID = "27483"
try:
    CLIENT_SECRET = st.secrets["TIENDANUBE_CLIENT_SECRET"]
except:
    CLIENT_SECRET = os.getenv("TIENDANUBE_CLIENT_SECRET", "")

# --- 5. DICCIONARIO MULTILINGÜE ---
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
        "criticos_tit": "🔎 Productos Críticos ",
        "btn_alerta": "🔔 Activar Monitor de Alertas Críticas"
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
        "criticos_tit": "🔎 Produtos Críticos",
        "btn_alerta": "🔔 Ativar Monitor de Alertas Críticas"
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
        "criticos_tit": "🔎 Critical Products",
        "btn_alerta": "🔔 Activate Critical Alert Monitor"
    }
}

# --- 6. FUNCIONES ---
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

# --- 7. BARRA LATERAL ---
with st.sidebar:
    st.markdown("""<div style="text-align: center;"><img src="https://imgur.com/YrVO3ZF.jpeg" style="width: 100%; border-radius:20px;"></div>""", unsafe_allow_html=True)
    idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"])
    alto_contraste = st.toggle("Modo Alto Contraste")
    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor", 1, 30, 7)
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_orders,read_products,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        if st.button("3. Vincular Tienda"):
            token_data = obtener_token_real(temp_code, CLIENT_ID, CLIENT_SECRET)
            if token_data and token_data.get("access_token"):
                st.session_state.token_ref = guardar_token_seguro(token_data.get("store_id"), token_data["access_token"])
                st.success("✅ Vinculado")

# --- 8. LÓGICA DE DATOS ---
t_act = textos[idioma]
df = calcular_motor_analisis(st.session_state.db_inventario.copy(), f_demanda)
autonomia_finita = np.isfinite(df["Autonomia"])
atrapado_val = (df.loc[(df["Autonomia"] > 60) & autonomia_finita, "Stock"] * df.loc[(df["Autonomia"] > 60) & autonomia_finita, "Costo"]).sum()
riesgo_val = (df.loc[(df["Autonomia"] < dias_entrega) & autonomia_finita, "V_Diaria"] * df.loc[(df["Autonomia"] < dias_entrega) & autonomia_finita, "Costo"] * 1.5).sum()
salud_neta = min(100, max(0, 100 - int(riesgo_val / 1000)))

# --- 9. INTERFAZ ---
st.markdown('<h1 style="background: linear-gradient(90deg, #0056ff, #00c6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem; font-weight: 800;">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.write(f"✨ {t_act['sub']}")

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[1]:
    c1, c2, c3 = st.columns(3)
    c1.metric(t_act["atrapado"], f"${atrapado_val:,.0f}")
    c2.metric(t_act["riesgo"], f"${riesgo_val:,.0f}")
    c3.metric(t_act["salud"], f"{salud_neta}%")
    st.bar_chart(df.set_index("Producto")["Autonomia"].replace(np.inf, 90))

with tabs[2]:
    st.subheader(t_act["est_tit"])
    condiciones = [df["Autonomia"] < dias_entrega, df["Autonomia"] > 60]
    df["Accion"] = np.select(condiciones, ["🚨 REABASTECER", "🔥 LIQUIDAR"], default="✅ ESTABLE")
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Accion"]].style.map(color_estado, subset=["Accion"]), use_container_width=True)
    
    # CORRECCIÓN DEL BOTÓN (Para evitar el texto extraño de DeltaGenerator)
    if st.button(t_act["btn_alerta"], use_container_width=True):
        en_riesgo = df[df["Accion"] == "🚨 REABASTECER"]
        if not en_riesgo.empty:
            ok, msg = disparar_alerta_critica(en_riesgo)
            if ok:
                st.error(msg)
                st.caption("📱 Simulando envío de reporte a WhatsApp del administrador...")
        else:
            st.info("✅ Todo estable. No hay productos críticos.")

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    equipo = [("Willan Álvarez", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"), ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"), ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg"), ("Edwing Garcia", "Ventas", "https://i.imgur.com/CQJu9xm.jpeg")]
    cols = st.columns(4)
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i]:
            st.image(img, width=100)
            st.bold(nombre)
            st.caption(cargo)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")