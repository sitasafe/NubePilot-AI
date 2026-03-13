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
        "btn_reporte": "📝 Generar Reporte en Tienda",
        "sync": "Sincronizando...",
        "sync_ok": "Sincronización Exitosa!",
        "equipo_tit": "👥 Equipo Multidisciplinario (Equipo 3)",
        "rep_proceso": "Generando página de reporte mediante API...",
        "rep_exito": "¡Página creada! El equipo del cliente ya puede verla en el administrador."
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas",
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa",
        "diferencia": "🎯 O que nos diferencia?",
        "dolor": "Hoje, milhares de donos de marcas passam **5 horas por semana** na frente de um Excel, tentando adivinhar o futuro. Flowmerce transforma dados de vendas em decisões automáticas.",
        "modelo_t": "### 💎 Modelo de Negócio (SaaS)",
        "starter": "- **Starter (Grátis):** Alertas básicos.",
        "growth": "- **Growth ($20 USD):** Predição IA.",
        "scale": "- **Scale (Premium):** Simulador de cenários.",
        "dato_cert": "💡 **Dado:** Reduzimos uma tarde inteira de trabalho a apenas 5 minutos de certeza.",
        "est_tit": "🧠 Estratégia e Inteligência de Dados",
        "sim_tit": "💎 Simulador de Liquidez (Nível Scale)",
        "sim_inv": "Investimento para Simular ($)",
        "sim_proj": "Vendas Projetadas",
        "sim_rec": "Recuperação em",
        "sim_dias": "dias",
        "btn_app": "🚀 Aplicar na Tiendanube",
        "btn_reporte": "📝 Gerar Relatório na Loja",
        "sync": "Sincronizando...",
        "sync_ok": "Sincronização com Sucesso!",
        "equipo_tit": "👥 Equipe Multidisciplinar (Equipe 3)",
        "rep_proceso": "Gerando página de relatório via API...",
        "rep_exito": "Página criada! A equipe já pode vê-la no painel."
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
        "btn_reporte": "📝 Generate Store Report",
        "sync": "Syncing...",
        "sync_ok": "Successful Synchronization!",
        "equipo_tit": "👥 Multidisciplinary Team (Team 3)",
        "rep_proceso": "Generating report page via API...",
        "rep_exito": "Page created! The team can now view it in the admin panel."
    }
}

# --- 4. FUNCIONES DE API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json().get("access_token") if response.status_code == 200 else None
    except: return None

def crear_pagina_reporte(token, contenido_html, titulo="Reporte Flowmerce"):
    # Si no hay token, simulamos éxito para la demo
    if not token or token == "demo_token":
        time.sleep(2) # Simular latencia de red
        return True
    
    url = "https://api.tiendanube.com/v1/pages"
    headers = {"Authentication": f"bearer {token}", "Content-Type": "application/json"}
    payload = {
        "page": {
            "publish": True,
            "i18n": {"es_AR": {"title": titulo, "content": contenido_html, "seo_handle": f"reporte-{int(time.time())}"}}
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        return response.status_code == 201
    except: return False

# --- 5. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })
if 'token' not in st.session_state:
    st.session_state.token = None

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
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
            with st.spinner("Validando..."):
                token_recibido = obtener_token_real(temp_code)
                if token_recibido:
                    st.session_state.token = token_recibido
                    st.success("Conectado ✅")
                else:
                    st.session_state.token = "demo_token" # Token fantasma para la demo
                    st.info("Modo Demo Activado 🧪")

# --- 7. ESTILOS CSS ---
st.markdown(f"""
<style>
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite; 
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    .stMetric {{ background: rgba(0, 86, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; }}
    .sim-box {{ background: linear-gradient(135deg, #0056ff 0%, #6200ea 100%); color: white; padding: 20px; border-radius: 15px; margin-top: 10px; }}
    .team-card-large {{ text-align: center; padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(0,86,255,0.1); }}
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
st.markdown(f"**✨ {t_act['sub']}**")

tabs = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tabs[0]:
    st.markdown(f"## {t_act['diferencia']}")
    col_v1, col_v2 = st.columns([0.6, 0.4])
    with col_v1:
        st.write(t_act["dolor"])
        st.info(t_act["dato_cert"])
    with col_v2:
        st.markdown(t_act["modelo_t"])
        st.write(t_act["starter"])
        st.write(t_act["growth"])
        st.write(t_act["scale"])

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
        with c_s1:
            st.markdown(f'<div class="sim-box"><small>{t_act["sim_proj"]}</small><h3>${sim_inv * (f_demanda * 1.8):,.0f} MXN</h3></div>', unsafe_allow_html=True)
        with c_s2:
            st.markdown(f'<div class="sim-box"><small>{t_act["sim_rec"]}</small><h3>{30/f_demanda:.1f} {t_act["sim_dias"]}</h3></div>', unsafe_allow_html=True)
    
    st.write("---")
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"
    
    df["Accion"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Accion"]])
    
    # --- BOTONES DE ACCIÓN ---
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button(t_act["btn_app"], use_container_width=True):
            with st.status(t_act["sync"]) as s:
                time.sleep(1.5)
                s.update(label=t_act["sync_ok"], state="complete")
                
    with c_btn2:
        # BOTÓN DE REPORTE CON SIMULACIÓN PARA DEMO
        if st.button(t_act["btn_reporte"], type="primary", use_container_width=True):
            # Usar token de sesión o el de demo
            current_token = st.session_state.token if st.session_state.token else "demo_token"
            
            with st.status(t_act["rep_proceso"]) as s:
                # Contenido HTML para la página
                html_body = f"""
                <div style='font-family:sans-serif; padding:20px;'>
                    <h2>Análisis de Liquidez Flowmerce</h2>
                    <p>Estado de Salud: <b>{max(0, 100-int(riesgo_val/1000))}%</b></p>
                    <hr>
                    <p>Alerta: Tienes ${atrapado_val} MXN en productos sin rotación.</p>
                </div>
                """
                exito = crear_pagina_reporte(current_token, html_body)
                
                if exito:
                    s.update(label=t_act["rep_exito"], state="complete")
                    st.balloons()
                    st.success(f"🔗 [Ver en Tienda (Simulado)](https://www.tiendanube.com/admin/pages/)")
                else:
                    st.error("Error de conexión con la API de Tiendanube.")

with tabs[3]:
    st.markdown(f"### {t_act['equipo_tit']}")
    # Lista de equipo reducida para ejemplo
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram Cabrera", "Organización", "https://i.imgur.com/eamMDmE.jpeg")
    ]
    cols = st.columns(4)
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i]:
            st.markdown(f"""<div class="team-card-large">
                <img src="{img}" style="width:80px; height:80px; border-radius:50%; object-fit:cover; margin-bottom:10px;">
                <br><b>{nombre}</b><br><small>{cargo}</small></div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
