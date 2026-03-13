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

# --- 3. DICCIONARIO MULTILINGÜE INTEGRAL ---
textos = {
    "Español": {
        "sub": "Donde los datos se convierten en ventas",
        "tab0": "🚀 Nuestra Visión", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estrategia", "tab3": "👥 Equipo",
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja",
        "vision_t": "🎯 ¿Qué nos diferencia?",
        "vision_p": "Tu negocio es un ritmo, no una adivinanza. Flowmerce transforma datos en decisiones automáticas.",
        "modelo_t": "💎 Modelo de Negocio",
        "funciona_t": "⚙️ ¿Cómo funciona?",
        "sim_t": "💎 Simulador de Liquidez (Nivel Scale)",
        "sim_inv": "Inversión a Simular ($)",
        "sim_ret": "Ventas Proyectadas",
        "sim_dias": "Recuperación en",
        "rec_t": "🤖 Recomendaciones Automáticas",
        "btn_sync": "🚀 Aplicar a Tiendanube",
        "equipo_t": "👥 Equipo Multidisciplinario (Equipo 3)"
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas",
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa",
        "vision_t": "🎯 O que nos diferencia?",
        "vision_p": "Seu negócio é um ritmo, não uma adivinhação. Flowmerce transforma dados em decisões automáticas.",
        "modelo_t": "💎 Modelo de Negócio",
        "funciona_t": "⚙️ Como funciona?",
        "sim_t": "💎 Simulador de Liquidez (Nível Scale)",
        "sim_inv": "Investimento para Simular ($)",
        "sim_ret": "Vendas Projetadas",
        "sim_dias": "Recuperação em",
        "rec_t": "🤖 Recomendações Automáticas",
        "btn_sync": "🚀 Aplicar na Tiendanube",
        "equipo_t": "👥 Equipe Multidisciplinar (Equipe 3)"
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Our Vision", "tab1": "📊 Liquidity Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health",
        "vision_t": "🎯 What makes us different?",
        "vision_p": "Your business is a rhythm, not a guessing game. Flowmerce turns data into automated decisions.",
        "modelo_t": "💎 Business Model",
        "funciona_t": "⚙️ How it works?",
        "sim_t": "💎 Liquidity Simulator (Scale Level)",
        "sim_inv": "Investment to Simulate ($)",
        "sim_ret": "Projected Sales",
        "sim_dias": "Recovery in",
        "rec_t": "🤖 Automated Recommendations",
        "btn_sync": "🚀 Apply to Tiendanube",
        "equipo_t": "👥 Multidisciplinary Team (Team 3)"
    }
}

# --- 4. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

# --- 5. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
    st.write("---")
    idioma = st.selectbox("🌐 Language / Idioma", ["Español", "Português", "English"])
    t = textos[idioma] # Atajo para las traducciones
    
    st.markdown(f"### ⚙️ {t['funciona_t']}")
    f_demanda = st.slider("Demand factor", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time", 1, 30, 7)

# --- 6. ESTILOS CSS ---
st.markdown(f"""
<style>
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite; 
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    .team-card-large {{
        text-align: center; padding: 20px; border-radius: 25px;
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 86, 255, 0.2);
        transition: all 0.4s ease; min-height: 260px;
    }}
    .team-card-large:hover {{ transform: translateY(-10px); border-color: #0056ff; box-shadow: 0px 15px 30px rgba(0, 86, 255, 0.2); }}
    .stMetric {{ background: rgba(0, 86, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; }}
    .sim-box {{ background: linear-gradient(135deg, #0056ff 0%, #6200ea 100%); color: white; padding: 20px; border-radius: 15px; margin-top: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- 7. LÓGICA ---
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)
atrapado_val = (df[df["Autonomia"] > 60]["Stock"] * df[df["Autonomia"] > 60]["Costo"]).sum()
riesgo_val = (df[df["Autonomia"] < dias_entrega]["V_Diaria"] * df[df["Autonomia"] < dias_entrega]["Costo"] * 1.5).sum()

# --- 8. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown(f"**✨ {t['sub']}**")

tabs = st.tabs([t["tab0"], t["tab1"], t["tab2"], t["tab3"]])

# TAB 0: VISIÓN
with tabs[0]:
    st.markdown(f"## {t['vision_t']}")
    c1, c2 = st.columns([0.6, 0.4])
    with c1:
        st.write(t['vision_p'])
        st.info("💡 Flowmerce: Excel 5h ➡️ AI 5min.")
    with c2:
        st.markdown(f"### {t['modelo_t']}")
        st.write("SaaS: Starter (Free), Growth ($20), Scale (Premium)")

# TAB 1: MONITOR
with tabs[1]:
    col1, col2, col3 = st.columns(3)
    col1.metric(t["atrapado"], f"${float(atrapado_val):,.0f}")
    col2.metric(t["riesgo"], f"${float(riesgo_val):,.0f}", delta="!")
    col3.metric(t["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")
    st.area_chart(df.set_index("Producto")["Stock"])

# TAB 2: ESTRATEGIA (SIMULADOR Y TABLA)
with tabs[2]:
    st.subheader(t["sim_t"])
    with st.container():
        sim_inv = st.number_input(t["sim_inv"], value=50000)
        cs1, cs2 = st.columns(2)
        cs1.markdown(f'<div class="sim-box"><small>{t["sim_ret"]}</small><h3>${sim_inv * (f_demanda * 1.8):,.0f}</h3></div>', unsafe_allow_html=True)
        cs2.markdown(f'<div class="sim-box"><small>{t["sim_dias"]}</small><h3>{30/f_demanda:.1f} days</h3></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader(t["rec_t"])
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"
    df["Acción"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Acción"]])
    st.button(t["btn_sync"])

# TAB 3: EQUIPO (FOTO DE DALIA CORREGIDA)
with tabs[3]:
    st.markdown(f"### {t['equipo_t']}")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"), # URL Corregida
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
                    <img src="{img}" style="width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 3px solid #0056ff; margin-bottom: 10px;">
                    <br><strong>{nombre}</strong><br><small style="color:#0056ff;">{cargo}</small>
                </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
