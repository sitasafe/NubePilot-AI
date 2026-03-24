import streamlit as st
import pandas as pd
import numpy as np
import os
import importlib

# --- NUEVA SECCIÓN: INICIALIZACIÓN DE BASE DE DATOS ---
from app.core.database import engine, Base
from app.core import models # Esto asegura que Base conozca las tablas

# Creamos las tablas justo antes de que la app empiece a funcionar
Base.metadata.create_all(bind=engine)
# -----------------------------------------------------

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

# --- 1. CONFIGURACIÓN DE PÁGINA (Blindaje PWA/Mobile) ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# Inyección de metadatos para simular comportamiento de App Nativa
st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <link rel="apple-touch-icon" href="https://imgur.com/YrVO3ZF.jpeg">
    </head>
""", unsafe_allow_html=True)

# --- 2. CREDENCIALES TIENDANUBE ---
CLIENT_ID = "27483"
try:
    CLIENT_SECRET = st.secrets["TIENDANUBE_CLIENT_SECRET"]
except (KeyError, FileNotFoundError):
    CLIENT_SECRET = os.getenv("TIENDANUBE_CLIENT_SECRET", "")

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

# --- 4. FUNCIONES MODULARES (Arquitectura 5 estrellas) ---

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


def generar_reporte_ejecutivo_pdf(salud_caja, productos_criticos, impulso_demanda):
    fpdf_module = importlib.import_module("fpdf")
    pdf_cls = getattr(fpdf_module, "FPDF")

    if impulso_demanda >= 2.0:
        recomendacion = (
            "Demanda acelerada: aumentar inversion de inventario entre 20% y 30%."
        )
    elif impulso_demanda >= 1.2:
        recomendacion = (
            "Demanda en crecimiento: aumentar inversion de inventario entre 10% y 15%."
        )
    else:
        recomendacion = (
            "Demanda estable: mantener inversion base y priorizar liquidez."
        )

    pdf = pdf_cls()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Flowmerce - Reporte Ejecutivo", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, f"Salud de Caja actual: {salud_caja}%")
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Productos criticos por reabastecimiento:", ln=True)
    pdf.set_font("Helvetica", size=11)

    if productos_criticos.empty:
        pdf.multi_cell(0, 7, "- Sin productos criticos en este momento.")
    else:
        for _, row in productos_criticos.iterrows():
            producto = str(row["Producto"])
            autonomia = float(row["Autonomia"])
            stock = int(row["Stock"])
            pdf.multi_cell(
                0,
                7,
                f"- {producto}: autonomia {autonomia:.1f} dias | stock actual {stock}",
            )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Recomendacion de inversion:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, recomendacion)

    return bytes(pdf.output(dest="S"))

# --- 5. GESTIÓN DE MEMORIA ---
inicializar_estado_app()
if not st.session_state.token_ref and not st.session_state.tn_store_id:
    db_store_id, db_token_ref = obtener_ultima_tienda_vinculada()
    if db_store_id and db_token_ref:
        st.session_state.tn_store_id = db_store_id
        st.session_state.token_ref = db_token_ref

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
        st.session_state.tn_store_id = st.text_input("3. Store ID (opcional si vinculas)", value=st.session_state.tn_store_id)
        if st.button("3. Vincular Tienda"):
            token_data = obtener_token_real(temp_code, CLIENT_ID, CLIENT_SECRET)
            if token_data and token_data.get("access_token"):
                store_id_detectado = token_data.get("store_id") or st.session_state.tn_store_id
                st.session_state.token_ref = guardar_token_seguro(
                    store_id_detectado, token_data["access_token"]
                )
                if token_data.get("store_id"):
                    st.session_state.tn_store_id = token_data["store_id"]
                st.success("✅ Tienda vinculada y guardada en la base de datos real")
            else:
                st.session_state.token_ref = None
                st.info("Modo Demo ✅")
        if st.button("4. Sincronizar ahora", use_container_width=True):
            store_id = normalizar_store_id(st.session_state.tn_store_id)
            progress_bar = st.progress(0)
            progress_text = st.empty()
            if not store_id:
                progress_text.empty()
                progress_bar.empty()
                st.warning("No pude obtener un Store ID numérico. Vincula primero para autocompletarlo o pega el ID de Tiendanube.")
            else:
                if not st.session_state.token_ref:
                    st.session_state.token_ref = obtener_token_ref_desde_db(store_id)
            if store_id and st.session_state.token_ref:
                progress_text.write("Sincronizando...")

                def on_sync_progress(progress, message):
                    progress_bar.progress(max(0.0, min(1.0, float(progress))))
                    progress_text.write(message)

                st.session_state.tn_snapshot = obtener_snapshot_tiendanube(
                    store_id,
                    st.session_state.token_ref,
                    CLIENT_ID,
                    _progress_callback=on_sync_progress,
                )
                if st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("ok"):
                    progress_bar.progress(1.0)
                    progress_text.empty()
                    st.success("Snapshot actualizado")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "rate_limit":
                    progress_text.empty()
                    st.warning("⏳ Límite de llamadas Tiendanube alcanzado. Espera 1 minuto e intenta de nuevo.")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "unauthorized":
                    progress_text.empty()
                    st.warning("🔐 Token expirado o inválido. Vuelve a vincular la tienda.")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "invalid_store_id":
                    progress_text.empty()
                    st.warning("Store ID o token inválido. Vuelve a vincular la tienda.")
                else:
                    progress_text.empty()
                    st.warning("No se pudo actualizar el snapshot. Verifica Store ID y permisos.")
            elif store_id:
                progress_text.empty()
                progress_bar.empty()
                st.info("Vincula una tienda real para sincronizar datos.")

# --- 7. ESTILOS ---
bg_overlay = "rgba(255, 255, 255, 0.7)" if not alto_contraste else "rgba(0, 0, 0, 0.9)"
text_color = "#1E1E1E" if not alto_contraste else "#FFFFFF"

st.markdown(f"""
<style>
    @keyframes gradient-move {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    @keyframes clouds-up {{ 0% {{ transform: translateY(100vh); opacity: 0; }} 100% {{ transform: translateY(-100vh); opacity: 0; }} }}
    .cloud-effect {{ position: fixed; font-size: 50px; z-index: 9999; pointer-events: none; animation: clouds-up 4s ease-in forwards; }}
    .stApp {{ background: linear-gradient({bg_overlay}, {bg_overlay}), url("https://imgur.com/gQ7yynl.jpeg"); background-attachment: fixed; background-size: cover; }}
    .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem !important; font-weight: 800; animation: gradient-move 3s linear infinite; }}
    div[data-testid="stMetric"], .stTable, .team-card-large, div[data-testid="stExpander"] {{ background-color: white !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important; }}
    div[data-testid="stTabs"] {{ background-color: rgba(255, 255, 255, 0.95) !important; padding: 30px !important; border-radius: 20px !important; }}
</style>
""", unsafe_allow_html=True)

# --- 8. EJECUCIÓN DEL MOTOR ---
t_act = textos[idioma]
snap = st.session_state.tn_snapshot
if snap and snap.get("ok") and snap.get("products"):
    df_source = extraer_inventario_desde_snapshot(snap)
else:
    df_source = st.session_state.db_inventario.copy()
df = calcular_motor_analisis(df_source, f_demanda)
autonomia_finita = np.isfinite(df["Autonomia"])

atrapado_mask = (df["Autonomia"] > 60) & autonomia_finita
riesgo_mask = (df["Autonomia"] < dias_entrega) & autonomia_finita
atrapado_val = (df.loc[atrapado_mask, "Stock"] * df.loc[atrapado_mask, "Costo"]).sum()
riesgo_val = (df.loc[riesgo_mask, "V_Diaria"] * df.loc[riesgo_mask, "Costo"] * 1.5).sum()
salud_neta = min(100, max(0, 100 - int(riesgo_val / 1000)))

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

c_enc1, c_enc2 = st.columns([0.8, 0.2])
with c_enc1: 
    st.markdown(f"<div style='background:white; padding:10px 20px; border-radius:10px; display:inline-block; color:{text_color}; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;'><strong>✨ {t_act['sub']}</strong></div>", unsafe_allow_html=True)

with c_enc2: 
    if MIC_AVAILABLE:
        audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')
        if audio_data:
            st.toast(t_act["escuchando"])
            st.info(f"{t_act['voz_ok']} [procesamiento de voz no implementado aun]")

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
    if st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("ok"):
        s1, s2, s3 = st.columns(3)
        s1.metric("Productos Tiendanube", f"{st.session_state.tn_snapshot['products_count']}")
        s2.metric("Órdenes Tiendanube", f"{st.session_state.tn_snapshot['orders_count']}")
        s3.metric("Pago confirmado", f"{st.session_state.tn_snapshot['paid_rate']:.1f}%")
        st.caption("Datos cacheados por 60 segundos para respuesta instantánea.")

    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{salud_neta}%")
    st.progress(min(1.0, max(0.0, salud_neta / 100.0))) # Indicador visual de salud
    
    st.write("### 📈 Autonomía de Inventario (Días)")
    df_chart = df.copy()
    df_chart["Autonomia"] = df_chart["Autonomia"].replace(np.inf, 90)
    st.bar_chart(df_chart.set_index("Producto")["Autonomia"])

with tabs[2]:
    st.subheader(t_act["est_tit"])
    vigilancia_activa = st.toggle("🛰️ Modo Vigilancia Activa")
    with st.expander(t_act["sim_tit"], expanded=True):
        sim_inv = st.number_input(t_act["sim_inv"], value=50000)
        c_s1, c_s2 = st.columns(2)
        with c_s1: st.markdown(f'<div style="background: linear-gradient(135deg, #0056ff 0%, #6200ea 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;"><small>{t_act["sim_proj"]}</small><h3>${sim_inv * (f_demanda * 1.8):,.0f} MXN</h3></div>', unsafe_allow_html=True)
        with c_s2: st.markdown(f'<div style="background: linear-gradient(135deg, #00c6ff 0%, #0056ff 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;"><small>{t_act["sim_rec"]}</small><h3>{30/f_demanda:.1f} {t_act["sim_dias"]}</h3></div>', unsafe_allow_html=True)
    
    st.write("---")
    condiciones = [df["Autonomia"] < dias_entrega, df["Autonomia"] > 60]
    acciones = ["🚨 REABASTECER", "🔥 LIQUIDAR"]
    df["Accion"] = np.select(condiciones, acciones, default="✅ ESTABLE")
    
    # Tabla con colores (Efecto SaaS Profesional)
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Accion"]].style.map(color_estado, subset=["Accion"]), use_container_width=True)

    # Ranking Crítico (Wow Moment)
    st.write(f"### {t_act['criticos_tit']}")
    criticos = df[np.isfinite(df["Autonomia"])].sort_values("Autonomia").head(2)
    st.table(criticos[["Producto", "Autonomia", "Stock"]])

    en_riesgo = df[df["Accion"] == "🚨 REABASTECER"].copy()
    riesgo_actual_set = set(en_riesgo["Producto"].astype(str).tolist())
    if "riesgo_prev_set" not in st.session_state:
        st.session_state.riesgo_prev_set = set()

    if vigilancia_activa:
        nuevos_en_riesgo = riesgo_actual_set - st.session_state.riesgo_prev_set
        if nuevos_en_riesgo:
            nuevos_df = en_riesgo[en_riesgo["Producto"].astype(str).isin(nuevos_en_riesgo)]
            ok_alerta_auto, mensaje_alerta_auto = disparar_alerta_critica(nuevos_df)
            st.markdown(
                """
                <style>
                @keyframes pulse-alert {
                    0% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.02); opacity: 0.9; }
                    100% { transform: scale(1); opacity: 1; }
                }
                div[data-testid="stAlert"] {
                    animation: pulse-alert 1.1s ease-in-out infinite;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            if ok_alerta_auto:
                st.error(mensaje_alerta_auto)
                st.caption(
                    "Simulando envío de reporte a WhatsApp del administrador..."
                )
            else:
                st.warning(mensaje_alerta_auto)
        st.session_state.riesgo_prev_set = riesgo_actual_set
    else:
        st.session_state.riesgo_prev_set = riesgo_actual_set

    if st.button("🔔 Activar Monitor de Alertas Críticas", use_container_width=True):
        if en_riesgo.empty:
            st.info("No hay productos críticos por reabastecer en este momento.")
        else:
            ok_alerta, mensaje_alerta = disparar_alerta_critica(en_riesgo)
            st.markdown(
                """
                <style>
                @keyframes pulse-alert {
                    0% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.02); opacity: 0.9; }
                    100% { transform: scale(1); opacity: 1; }
                }
                div[data-testid="stAlert"] {
                    animation: pulse-alert 1.1s ease-in-out infinite;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            if ok_alerta:
                st.error(mensaje_alerta)
                st.caption(
                    "Simulando envío de reporte a WhatsApp del administrador..."
                )
            else:
                st.warning(mensaje_alerta)
    
    def animar_nubes():
        st.empty().markdown('<div class="cloud-effect" style="left: 50%;">☁️</div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button(t_act["btn_app"], use_container_width=True):
            animar_nubes()
            st.success(t_act["sync_ok"])
    with col_b2:
        csv = exportar_csv(df)
        if st.download_button(label=t_act["btn_reporte"], data=csv, file_name='Reporte_Flowmerce.csv', use_container_width=True):
            st.toast(t_act["rep_exito"])

    reporte_pdf = generar_reporte_ejecutivo_pdf(salud_neta, en_riesgo, f_demanda)
    st.download_button(
        "📄 Descargar Reporte Ejecutivo (PDF)",
        data=reporte_pdf,
        file_name="Reporte_Ejecutivo_Flowmerce.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

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
                st.markdown(f"""<div class="team-card-large" style="text-align:center;">
                    <img src="{img}" style="width: 110px; height: 110px; border-radius: 50%; object-fit: cover;">
                    <br><strong>{nombre}</strong><br><small style="color:#0056ff;">{cargo}</small>
                </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3 | TiendaNube")