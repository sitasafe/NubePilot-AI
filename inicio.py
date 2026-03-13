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

# --- 3. DICCIONARIO MULTILINGÜE (Actualizado con tu Slogan) ---
textos = {
    "Español": {
        "sub": "Donde los datos se convierten en ventas",
        "tab1": "📊 Monitor de Liquidez & ROI", "tab2": "🧠 Estrategia IA", "tab3": "👥 Equipo",
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja"
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas",
        "tab1": "📊 Monitor de Liquidez e ROI", "tab2": "🧠 Estratégia IA", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa"
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab1": "📊 Liquidity & ROI Monitor", "tab2": "🧠 AI Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health"
    }
}

# --- 4. FUNCIONES DE API ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {
        "client_id": int(CLIENT_ID),
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code.strip()
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("access_token") if response.status_code == 200 else None
    except requests.RequestException:
        return None

# --- 5. GESTIÓN DE MEMORIA (SESSION STATE) ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    st.write("---")

    with st.expander("🌐 Accesibilidad e Idioma", expanded=True):
        idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda (Factor)", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor (Días)", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_orders,read_products,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        
        if st.button("3. Vincular Tienda"):
            token = obtener_token_real(temp_code)
            if token:
                st.session_state.token_tienda = token
                st.success("¡Conexión Establecida! ✅")
            else:
                st.error("Error en vinculación.")

    st.divider()
    st.markdown("### 📲 Notificaciones")
    st.toggle("Plan del día a WhatsApp", value=True)
    st.toggle("Alertas SMS (Zonas sin datos)", value=False)

# --- 7. ESTILOS CSS (ALINEADO A LA IZQUIERDA) ---
extra_styles = ""
if lectura_facil: extra_styles += "html, body, p, div { font-size: 1.4rem !important; line-height: 1.8 !important; }"
if alto_contraste: extra_styles += ".stApp { background: #000 !important; color: #fff !important; } .team-card-large { border: 2px solid white !important; }"

st.markdown(f"""
<style>
    {extra_styles}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; 
        animation: gradient-move 4s ease infinite; 
        text-align: left;
        margin-bottom: 0px;
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    
    .team-card-large {{
        text-align: center; padding: 25px; border-radius: 25px;
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 86, 255, 0.2);
        transition: all 0.4s ease; margin-bottom: 20px;
    }}
    .team-card-large:hover {{ transform: translateY(-10px); border-color: #0056ff; box-shadow: 0px 15px 30px rgba(0, 86, 255, 0.2); }}
    .stMetric {{ background: rgba(0, 86, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE CÁLCULO ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], np.inf)

filtro_atrapado = df["Autonomia"] > 60
atrapado_val = (df.loc[filtro_atrapado, "Stock"] * df.loc[filtro_atrapado, "Costo"]).sum()

filtro_riesgo = df["Autonomia"] < dias_entrega
riesgo_val = (df.loc[filtro_riesgo, "V_Diaria"] * df.loc[filtro_riesgo, "Costo"] * 1.5).sum()

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce IA</h1>', unsafe_allow_html=True)

# Slogan y Botón de Voz en una fila alineada a la izquierda
c_voz1, c_voz2 = st.columns([0.8, 0.2])
with c_voz1:
    st.markdown(f"**✨ {t_act['sub']}**")
with c_voz2:
    mic_recorder(start_prompt="🎤 Voz", stop_prompt="🛑", key='rec')

tab1, tab2, tab3 = st.tabs([t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="¡Alerta!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{max(0, 100-(dias_entrega*2))}%")

    st.write("---")
    st.subheader("📈 Análisis de Capital por Producto")
    df["Capital_Invertido"] = df["Stock"] * df["Costo"]
    st.area_chart(df.set_index("Producto")["Capital_Invertido"])

with tab2:
    st.subheader("🤖 Decisiones Automatizadas por IA")
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 COMPRAR YA"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR STOCK"
        return "✅ ESTABLE"

    df["Acción Sugerida"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Autonomia", "Acción Sugerida"]])
    
    if st.button("🚀 Sincronizar con Tiendanube"):
        with st.status("Procesando..."): time.sleep(1.5)
        st.balloons()

with tab3:
    st.markdown("### 👥 Equipo Multidisciplinario (Equipo 3)")
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
                st.markdown(f"""
                <div class="team-card-large">
                    <img src="{img}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #0056ff; margin-bottom: 15px;">
                    <br><strong>{nombre}</strong><br><small style="color:#0056ff;">{cargo}</small>
                </div>
                """, unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce IA | Hackathon UTEL 2026 | Equipo 3")

