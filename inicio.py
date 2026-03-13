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

# --- 7. ESTILOS CSS (RECUPERANDO EFECTOS BLOQUES E IMPULSA IA) ---
extra_styles = ""
if lectura_facil: 
    extra_styles += "html, body, [class*='st-'] { font-size: 1.5rem !important; line-height: 2 !important; }"
if alto_contraste: 
    extra_styles += """
    .stApp { background: #000000 !important; color: #FFFFFF !important; }
    .problem-box, .team-card-large { background: #222222 !important; border: 2px solid white !important; }
    h1, h2, h3, p, span { color: #FFFFFF !important; }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp {{ font-family: 'Inter', sans-serif; }}

    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; font-weight: 800; animation: gradient-move 4s ease infinite;
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}

    /* ESTILO DE BLOQUES RECUPERADO */
    .problem-box {{
        background-color: white; padding: 25px; border-radius: 20px; border-left: 8px solid #0056ff;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05); height: 100%; transition: all 0.3s ease; color: #1a1c2e;
    }}
    .problem-box:hover {{ background: #fdfdff; border-left: 8px solid #00c6ff; transform: translateX(10px); }}

    /* TARJETAS DE EQUIPO GRANDES RECUPERADAS */
    .team-card-large {{
        text-align: center; padding: 35px; border-radius: 30px; background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px); border: 1px solid rgba(0, 86, 255, 0.1);
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05); margin-bottom: 25px; transition: all 0.4s ease;
    }}
    .team-card-large:hover {{ transform: translateY(-15px) scale(1.02); border: 1px solid #0056ff; box-shadow: 0px 30px 60px rgba(0, 86, 255, 0.15); }}

    /* EFECTO NUBES */
    @keyframes cloud-up {{
        0% {{ transform: translateY(100vh); opacity: 0; }}
        10% {{ opacity: 0.8; }} 90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-100vh); opacity: 0; }}
    }}
    .cloud-ascend {{
        position: fixed; bottom: 0; font-size: 5rem; z-index: 9999;
        pointer-events: none; animation: cloud-up 3s linear infinite;
    }}
    
    {extra_styles}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE CÁLCULO ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)
atrapado_val = df[df["Autonomia"] > 60][["Stock", "Costo"]].product(axis=1).sum()
riesgo_val = df[df["Autonomia"] < dias_entrega][["V_Diaria", "Costo"]].product(axis=1).sum() * 1.5

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
c_h1, c_h2 = st.columns([0.8, 0.2])
with c_h1: st.subheader(f"✨ {t_act['sub']}")
with c_h2: mic_recorder(start_prompt="🎤 Voz", stop_prompt="🛑", key='rec')

tab0, tab1, tab2, tab3 = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab0:
    st.markdown("### 🎯 Nuestra Visión Estratégica")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="problem-box">
            <h4 style="color:#0056ff;">📊 El Desafío</h4>
            <p>Miles de marcas entierran capital en productos que no rotan, asfixiando su crecimiento financiero.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="problem-box">
            <h4 style="color:#0056ff;">🤖 Inteligencia</h4>
            <p>Usamos IA para predecir el ritmo de venta y sincronizar tu stock con la demanda real del mercado.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="problem-box">
            <h4 style="color:#0056ff;">💎 Modelo SaaS</h4>
            <p>Desde alertas gratuitas hasta simulaciones avanzadas para escalar tu Tiendanube al siguiente nivel.</p>
        </div>""", unsafe_allow_html=True)

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="¡Alerta!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%")
    st.write("---")
    st.subheader("📈 Proyección de Capital")
    df["Capital_Invertido"] = df["Stock"] * df["Costo"]
    st.area_chart(df.set_index("Producto")["Capital_Invertido"])

with tab2:
    st.subheader("🤖 Recomendaciones IA")
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"

    df["Acción Sugerida"] = df.apply(determinar_accion, axis=1)
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Acción Sugerida"]], use_container_width=True)
    
    if st.button("🚀 Sincronizar con Tiendanube (Nubes)"):
        cloud_placeholder = st.empty()
        with st.status("Subiendo datos a la nube...", expanded=True) as s:
            cloud_placeholder.markdown("""
                <div class="cloud-ascend" style="left: 10%; animation-duration: 2.5s;">☁️</div>
                <div class="cloud-ascend" style="left: 40%; animation-duration: 3s;">☁️</div>
                <div class="cloud-ascend" style="left: 70%; animation-duration: 2s;">☁️</div>
            """, unsafe_allow_html=True)
            time.sleep(3)
            s.update(label="¡Sincronización Exitosa! ☁️", state="complete")
        cloud_placeholder.empty()
        st.balloons()

with tab3:
    st.markdown("### 👥 Equipo Multidisciplinario (Equipo 3)")
    equipo = [
        ("Willan Álvarez.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2B8L8.jpeg"),
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 5px solid #0056ff; margin-bottom: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                    <br><strong style="font-size:1.2rem;">{nombre}</strong><br><small style="color:#0056ff; font-weight:bold;">{cargo}</small>
                </div>
                """, unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
