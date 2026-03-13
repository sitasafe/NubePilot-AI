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
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja"
    },
    "Português": {
        "sub": "Onde os datos se transformam em vendas",
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa"
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Our Vision", "tab1": "📊 Liquidity Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health"
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
        "Stock": [15, 95, 45, 4], "Ventas_30d": [45, 10, 30, 42], "Costo": [1200, 350, 150, 890]
    })

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
    st.write("---")
    with st.expander("🌐 Accesibilidad e Idioma", expanded=True):
        idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda (Factor)", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor (Días)", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_products,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token: st.success("¡Conexión Exitosa! ✅")

# --- 7. ESTILOS CSS UNIFICADOS (Efectos Bloques + Colores) ---
extra_styles = ""
if lectura_facil: extra_styles += "html, body, p, div { font-size: 1.4rem !important; line-height: 1.8 !important; }"
if alto_contraste: 
    extra_styles += ".stApp { background: #000 !important; color: #fff !important; } .problem-box, .team-card-large { border: 2px solid white !important; background: #111 !important; }"

st.markdown(f"""
<style>
    {extra_styles}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; animation: gradient-move 4s ease infinite; 
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    
    /* Estilo de Bloques (Efecto Impulsa IA) */
    .problem-box {{
        background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.03); transition: all 0.3s ease; height: 100%; color: #333;
    }}
    .problem-box:hover {{ transform: translateX(10px); border-left: 8px solid #00c6ff; background: #fdfdff; }}

    /* Estilo Equipo Potenciado */
    .team-card-large {{
        text-align: center; padding: 30px; border-radius: 30px; background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 86, 255, 0.2); transition: all 0.4s ease; margin-bottom: 20px;
    }}
    .team-card-large:hover {{ transform: translateY(-15px); border-color: #0056ff; box-shadow: 0px 20px 40px rgba(0, 86, 255, 0.2); }}

    /* Efecto Nubes */
    @keyframes cloud-up {{
        0% {{ transform: translateY(100vh); opacity: 0; }}
        10% {{ opacity: 0.8; }} 90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-100vh); opacity: 0; }}
    }}
    .cloud-ascend {{
        position: fixed; bottom: 0; font-size: 5rem; z-index: 9999;
        pointer-events: none; animation: cloud-up 3s linear infinite;
    }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)
atrapado_val = df[df["Autonomia"] > 60][["Stock", "Costo"]].product(axis=1).sum()
riesgo_val = df[df["Autonomia"] < dias_entrega][["V_Diaria", "Costo"]].product(axis=1).sum() * 1.5

# --- 9. CUERPO ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
c_h1, c_h2 = st.columns([0.8, 0.2])
with c_h1: st.markdown(f"**✨ {t_act['sub']}**")
with c_h2: mic_recorder(start_prompt="🎤 Voz", stop_prompt="🛑", key='rec')

tab0, tab1, tab2, tab3 = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab0:
    st.markdown("## 🎯 Nuestra Visión")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="problem-box">
            <h4>El Problema</h4>
            <p>El 30% del capital de las PyMEs está atrapado en stock que no se mueve, mientras pierden ventas por falta de productos estrella.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="problem-box">
            <h4>Nuestra Solución</h4>
            <p>IA predictiva que conecta tu inventario con la demanda real, automatizando compras y liquidaciones.</p>
        </div>""", unsafe_allow_html=True)

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${atrapado_val:,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${riesgo_val:,.0f} MXN", delta="¡Crítico!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")
    st.area_chart(df.set_index("Producto")["Stock"])

with tab2:
    st.subheader("🤖 Estrategia de Ejecución")
    if st.button("🚀 Sincronizar y Aplicar con Nubes"):
        cloud_placeholder = st.empty()
        with st.status("Subiendo datos a la nube...", expanded=True) as s:
            cloud_placeholder.markdown("""
                <div class="cloud-ascend" style="left: 15%; animation-duration: 2.5s;">☁️</div>
                <div class="cloud-ascend" style="left: 45%; animation-duration: 3s;">☁️</div>
                <div class="cloud-ascend" style="left: 75%; animation-duration: 2.2s;">☁️</div>
            """, unsafe_allow_html=True)
            time.sleep(3)
            s.update(label="¡Tienda Actualizada! ☁️", state="complete")
        cloud_placeholder.empty()
        st.balloons()

with tab3:
    st.markdown("### 👥 Equipo 3")
    equipo = [("Willan Álvarez.", "Architect", "https://i.imgur.com/CSH9Af7.jpeg"), ("Dalia R.", "PM", "https://i.imgur.com/4O2B8L8.jpeg"), ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"), ("Jiram Cabrera", "Org", "https://i.imgur.com/eamMDmE.jpeg")]
    cols = st.columns(4)
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i]:
            st.markdown(f"""<div class="team-card-large">
                <img src="{img}" style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid #0056ff;">
                <br><strong>{nombre}</strong><br><small>{cargo}</small>
            </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
