import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# --- INYECCIÓN DE METADATOS MOBILE (OPTIMIZACIÓN) ---
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="https://imgur.com/YrVO3ZF.jpeg">
""", unsafe_allow_html=True)

# --- 2. CREDENCIALES TIENDANUBE (SEGURO) ---
CLIENT_ID = st.secrets.get("CLIENT_ID", "27483")
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", "demo_secret")

# --- 3. DICCIONARIO MULTILINGÜE ---
textos = {
    "Español": {
        "sub": "Donde los datos se convierten en ventas",
        "tab0": "🚀 Visión", "tab1": "📊 Monitor", "tab2": "🧠 Estrategia", "tab3": "👥 Equipo",
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
        "btn_reporte": "📝 Generar Reporte",
        "sync_ok": "Sincronización Exitosa!",
        "equipo_tit": "👥 Nuestro Equipo",
        "rep_exito": "¡Reporte listo! ✅",
        "escuchando": "🎙️ Analizando voz...",
        "voz_ok": "✅ Comando recibido: "
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas",
        "tab0": "🚀 Visão", "tab1": "📊 Monitor", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa",
        "diferencia": "🎯 O que nos diferencia?",
        "dolor": "Hoje, milhares de donos de marcas passam **5 horas por semana** na frente de um Excel. Flowmerce transforma dados em decisões.",
        "modelo_t": "### 💎 Modelo SaaS",
        "starter": "- **Starter (Grátis):** Alertas.",
        "growth": "- **Growth ($20):** IA.",
        "scale": "- **Scale (Premium):** Simulador.",
        "dato_cert": "💡 **Dado:** Reduzimos o trabalho para apenas 5 minutos.",
        "est_tit": "🧠 Estratégia e Inteligência",
        "sim_tit": "💎 Simulador (Nível Scale)",
        "sim_inv": "Investimento ($)",
        "sim_proj": "Vendas Projetadas",
        "sim_rec": "Recuperação em",
        "sim_dias": "dias",
        "btn_app": "🚀 Aplicar na Tiendanube",
        "btn_reporte": "📝 Gerar Relatório",
        "sync_ok": "Sucesso!",
        "equipo_tit": "👥 Equipe (Equipo 3)",
        "rep_exito": "Relatório pronto! ✅",
        "escuchando": "🎙️ Analisando voz...",
        "voz_ok": "✅ Recebido: "
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Vision", "tab1": "📊 Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health",
        "diferencia": "🎯 What makes us different?",
        "dolor": "Brand owners spend **5 hours per week** on Excel. Flowmerce automates decisions.",
        "modelo_t": "### 💎 SaaS Model",
        "starter": "- **Starter (Free):** Basic alerts.",
        "growth": "- **Growth ($20):** AI Prediction.",
        "scale": "- **Scale (Premium):** Scenario simulator.",
        "dato_cert": "💡 **Fact:** From an entire afternoon to 5 minutes.",
        "est_tit": "🧠 Data Strategy",
        "sim_tit": "💎 Simulator (Scale Level)",
        "sim_inv": "Investment ($)",
        "sim_proj": "Projected Sales",
        "sim_rec": "Recovery in",
        "sim_dias": "days",
        "btn_app": "🚀 Apply to Tiendanube",
        "btn_reporte": "📝 Generate Report",
        "sync_ok": "Success!",
        "equipo_tit": "👥 Team 3",
        "rep_exito": "Ready! ✅",
        "escuchando": "🎙️ Analyzing voice...",
        "voz_ok": "✅ Received: "
    }
}

# --- 4. OAUTH TIENDANUBE (MEJOR MANEJO DE ERRORES) ---
def obtener_token_real(code):

    if not code:
        return None

    url = "https://www.tiendanube.com/apps/authorize/token"

    payload = {
        "client_id": int(CLIENT_ID),
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code.strip()
    }

    try:
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")

        return None

    except requests.exceptions.RequestException:
        return None

# --- 5. SESSION STATE ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

if 'token_session' not in st.session_state:
    st.session_state.token_session = None

# --- 6. SIDEBAR ---
with st.sidebar:

    st.markdown("""
    <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        .logo-flow { animation: float 4s ease-in-out infinite; border-radius: 20px; }
    </style>

    <div style="text-align:center;">
        <img src="https://imgur.com/YrVO3ZF.jpeg" class="logo-flow" style="width:100%;">
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🌐 Accesibilidad e Idioma", expanded=True):
        idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")

    f_demanda = st.slider("Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor", 1, 30, 7)

    with st.expander("🔑 Conexión Tiendanube", expanded=True):

        st.link_button(
            "1. Autorizar App",
            f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_orders,read_products,write_products"
        )

        temp_code = st.text_input("2. Pega el Code:")

        if st.button("3. Vincular Tienda"):

            if not temp_code:
                st.warning("⚠️ Pega primero el code de autorización.")
            else:
                token = obtener_token_real(temp_code)

                if token:
                    st.session_state.token_session = token
                    st.success("✅ Tienda conectada correctamente")
                else:
                    st.session_state.token_session = "demo"
                    st.info("Modo Demo activado para simulación del hackathon ✅")

# --- 7. LÓGICA DE NEGOCIO ---
t_act = textos[idioma]

df = st.session_state.db_inventario.copy()

df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda

df["Autonomia"] = np.where(
    df["V_Diaria"] > 0,
    df["Stock"] / df["V_Diaria"],
    999
)

atrapado_val = (
    df[df["Autonomia"] > 60]["Stock"] *
    df[df["Autonomia"] > 60]["Costo"]
).sum()

riesgo_val = (
    df[df["Autonomia"] < dias_entrega]["V_Diaria"] *
    df[df["Autonomia"] < dias_entrega]["Costo"] *
    1.5
).sum()

# --- 8. INTERFAZ ---
st.title("🌊 Flowmerce")

st.caption(t_act["sub"])

audio_data = mic_recorder(start_prompt="🎤 Comando Voz", stop_prompt="🛑 Detener")

if audio_data:
    st.toast(t_act["escuchando"])
    time.sleep(1)
    st.info(f"{t_act['voz_ok']} 'Optimizar inventario'")

tabs = st.tabs([
    t_act["tab0"],
    t_act["tab1"],
    t_act["tab2"],
    t_act["tab3"]
])

# --- VISIÓN ---
with tabs[0]:

    st.markdown(f"## {t_act['diferencia']}")

    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        st.write(t_act["dolor"])
        st.info(t_act["dato_cert"])

    with col2:
        st.markdown(t_act["modelo_t"])
        st.write(
            f"{t_act['starter']}\n"
            f"{t_act['growth']}\n"
            f"{t_act['scale']}"
        )

# --- MONITOR ---
with tabs[1]:

    c1, c2, c3 = st.columns(3)

    c1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    c2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="!", delta_color="inverse")
    c3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")

    st.area_chart(df.set_index("Producto")["Stock"])

# --- ESTRATEGIA ---
with tabs[2]:

    st.subheader(t_act["est_tit"])

    with st.expander(t_act["sim_tit"], expanded=True):

        sim_inv = st.number_input(t_act["sim_inv"], value=50000)

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                t_act["sim_proj"],
                f"${sim_inv * (f_demanda * 1.8):,.0f}"
            )

        with c2:
            st.metric(
                t_act["sim_rec"],
                f"{30/max(f_demanda,0.1):.1f} {t_act['sim_dias']}"
            )

    def determinar_accion(row):

        if row["Autonomia"] < dias_entrega:
            return "🚨 REABASTECER"

        if row["Autonomia"] > 60:
            return "🔥 LIQUIDAR"

        return "✅ ESTABLE"

    df["Accion"] = df.apply(determinar_accion, axis=1)

    st.table(df[["Producto", "Stock", "Accion"]])

    col1, col2 = st.columns(2)

    with col1:

        if st.button(t_act["btn_app"]):
            st.success(t_act["sync_ok"])

    with col2:

        csv = df.to_csv(index=False).encode("utf-8")

        if st.download_button(
            label=t_act["btn_reporte"],
            data=csv,
            file_name="Reporte_Flowmerce.csv",
            mime="text/csv"
        ):
            st.toast(t_act["rep_exito"])

# --- EQUIPO ---
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

    cols = st.columns(4)

    for i, (nombre, cargo, img) in enumerate(equipo):

        with cols[i % 4]:

            st.markdown(
                f"""
                <div style="text-align:center;">
                <img src="{img}" style="width:80px;height:80px;border-radius:50%;">
                <br><strong>{nombre}</strong>
                <br><small>{cargo}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()

st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3 | TiendaNube |")
