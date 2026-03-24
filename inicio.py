import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import re
import uuid
try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

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
@st.cache_resource
def get_http_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session

@st.cache_resource
def get_token_vault():
    # Token storage in server memory to avoid exposing raw token in session_state.
    return {}

def guardar_token_seguro(token):
    token_ref = str(uuid.uuid4())
    get_token_vault()[token_ref] = token
    return token_ref

def obtener_token_seguro(token_ref):
    return get_token_vault().get(token_ref) if token_ref else None

def normalizar_store_id(raw_store_id):
    if raw_store_id is None:
        return ""
    text = str(raw_store_id).strip()
    if not text:
        return ""
    match = re.search(r"/(\d+)(?:/|$)", text)
    if match:
        return match.group(1)
    only_digits = re.sub(r"\D", "", text)
    return only_digits if only_digits else ""

def obtener_token_real(code):
    if not code or not CLIENT_SECRET:
        return None
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = get_http_session().post(url, json=payload, timeout=10)
        if response.status_code != 200:
            return None
        body = response.json()
        return {
            "access_token": body.get("access_token"),
            "store_id": str(body.get("user_id", "")).strip(),
        }
    except requests.RequestException:
        return None

def extraer_inventario_desde_snapshot(snapshot):
    products = snapshot.get("products", []) if snapshot else []
    rows = []
    for p in products:
        nombre = p.get("name", {})
        if isinstance(nombre, dict):
            nombre = nombre.get("es") or nombre.get("pt") or nombre.get("en") or p.get("handle") or "Producto"
        nombre = str(nombre) if nombre else "Producto"
        variants = p.get("variants", []) if isinstance(p.get("variants", []), list) else []
        stock_total = sum(int(v.get("stock", 0) or 0) for v in variants) if variants else int(p.get("stock", 0) or 0)
        rows.append({
            "Producto": nombre,
            "Stock": max(0, stock_total),
            "Ventas_30d": 0,
            "Ventas_7d": 0,
            "Costo": 0,
        })
    if not rows:
        return pd.DataFrame(columns=["Producto", "Stock", "Ventas_30d", "Ventas_7d", "Costo"])
    return pd.DataFrame(rows)

@st.cache_data(ttl=60)
def obtener_snapshot_tiendanube(store_id, token_ref):
    access_token = obtener_token_seguro(token_ref)
    normalized_store_id = normalizar_store_id(store_id)
    if not normalized_store_id or not access_token:
        return {"ok": False, "error": "invalid_store_id"}

    base_url = f"https://api.tiendanube.com/v1/{normalized_store_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": f"Flowmerce ({CLIENT_ID})",
    }
    session = get_http_session()
    try:
        products = []
        page = 1
        while True:
            r_products = session.get(f"{base_url}/products", headers=headers, params={"page": page, "per_page": 50}, timeout=10)
            if r_products.status_code == 401:
                return {"ok": False, "error": "unauthorized"}
            if r_products.status_code == 429:
                return {"ok": False, "error": "rate_limit"}
            if r_products.status_code != 200:
                return {"ok": False, "status_products": r_products.status_code}
            page_items = r_products.json() if isinstance(r_products.json(), list) else []
            products.extend(page_items)
            if len(page_items) < 50 or page >= 5:
                break
            page += 1

        orders = []
        page = 1
        while True:
            r_orders = session.get(f"{base_url}/orders", headers=headers, params={"page": page, "per_page": 50}, timeout=10)
            if r_orders.status_code == 401:
                return {"ok": False, "error": "unauthorized"}
            if r_orders.status_code == 429:
                return {"ok": False, "error": "rate_limit"}
            if r_orders.status_code != 200:
                return {"ok": False, "status_orders": r_orders.status_code}
            page_items = r_orders.json() if isinstance(r_orders.json(), list) else []
            orders.extend(page_items)
            if len(page_items) < 50 or page >= 5:
                break
            page += 1

        total_orders = len(orders)
        paid_orders = sum(1 for o in orders if str(o.get("payment_status", "")).lower() == "paid")
        return {
            "ok": True,
            "products": products,
            "products_count": len(products),
            "orders_count": total_orders,
            "paid_rate": (paid_orders / total_orders * 100) if total_orders else 0.0,
        }
    except requests.RequestException:
        return {"ok": False, "error": "network"}

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

# --- 5. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Ventas_7d": [11, 2, 8, 12],
        "Costo": [1200, 350, 150, 890]
    })
if "token_ref" not in st.session_state:
    st.session_state.token_ref = None
if "tn_store_id" not in st.session_state:
    st.session_state.tn_store_id = ""
if "tn_snapshot" not in st.session_state:
    st.session_state.tn_snapshot = None

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
            token_data = obtener_token_real(temp_code)
            if token_data and token_data.get("access_token"):
                st.session_state.token_ref = guardar_token_seguro(token_data["access_token"])
                if token_data.get("store_id"):
                    st.session_state.tn_store_id = token_data["store_id"]
                    st.success(f"✅ Tienda vinculada. Store ID detectado: {token_data['store_id']}")
                else:
                    st.success("✅ Tienda vinculada.")
            else:
                st.session_state.token_ref = None
                st.info("Modo Demo ✅")
        if st.button("4. Sincronizar ahora", use_container_width=True):
            store_id = normalizar_store_id(st.session_state.tn_store_id)
            if not store_id:
                st.warning("No pude obtener un Store ID numérico. Vincula primero para autocompletarlo o pega el ID de Tiendanube.")
            elif st.session_state.token_ref:
                with st.spinner("Sincronizando Tiendanube..."):
                    st.session_state.tn_snapshot = obtener_snapshot_tiendanube(store_id, st.session_state.token_ref)
                if st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("ok"):
                    st.success("Snapshot actualizado")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "rate_limit":
                    st.warning("⏳ Límite de llamadas Tiendanube alcanzado. Espera 1 minuto e intenta de nuevo.")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "unauthorized":
                    st.warning("🔐 Token expirado o inválido. Vuelve a vincular la tienda.")
                elif st.session_state.tn_snapshot and st.session_state.tn_snapshot.get("error") == "invalid_store_id":
                    st.warning("Store ID o token inválido. Vuelve a vincular la tienda.")
                else:
                    st.warning("No se pudo actualizar el snapshot. Verifica Store ID y permisos.")
            else:
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
