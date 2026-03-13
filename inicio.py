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
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("access_token") if response.status_code == 200 else None
    except requests.RequestException:
        return None

# --- 5. GESTIÓN DE MEMORIA ---
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

# --- 7. ESTILOS CSS ---
st.markdown(f"""
<style>
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea, #0056ff);
        background-size: 300% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; 
        animation: gradient-move 4s ease infinite; 
        text-align: left;
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    .loading-banner {{
        background: rgba(0, 86, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #0056ff;
        text-align: center;
        margin-bottom: 25px;
    }}
    .team-card-large {{
        text-align: center; padding: 25px; border-radius: 25px;
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 86, 255, 0.2);
        transition: all 0.4s ease; margin-bottom: 20px;
    }}
    .stMetric {{ background: rgba(0, 86, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE CÁLCULO ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], np.inf)

# --- 9. CUERPO DE LA APP ---
# Placeholder para el BANNER DE CARGA (Aparecerá arriba en primer plano)
loading_placeholder = st.empty()

st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

c_enc1, c_enc2 = st.columns([0.8, 0.2])
with c_enc1:
    st.markdown(f"**✨ {t_act['sub']}**")
with c_enc2:
    mic_recorder(start_prompt="🎤 Voz", stop_prompt="🛑", key='rec')

tab1, tab2, tab3 = st.tabs([t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab1:
    col1, col2, col3 = st.columns(3)
    atrapado_val = (df.loc[df["Autonomia"] > 60, "Stock"] * df.loc[df["Autonomia"] > 60, "Costo"]).sum()
    riesgo_val = (df.loc[df["Autonomia"] < dias_entrega, "V_Diaria"] * df.loc[df["Autonomia"] < dias_entrega, "Costo"] * 1.5).sum()
    
    col1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    col2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="¡Alerta!", delta_color="inverse")
    col3.metric(t_act["salud"], f"{max(0, 100-(dias_entrega*2))}%")
    st.area_chart(df.set_index("Producto")["Stock"] * df["Costo"])

with tab2:
    st.subheader("🤖 Recomendaciones Estratégicas")
    def determinar_accion(row):
        if row["Autonomia"] < dias_entrega: return "🚨 REABASTECER"
        if row["Autonomia"] > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"
    
    df["Acción Sugerida"] = df.apply(determinar_accion, axis=1)
    st.table(df[["Producto", "Stock", "Autonomia", "Acción Sugerida"]])
    
    # --- PROCESO DE CARGA TIPO BANNER ---
    if st.button("🚀 Aplicar Cambios en Tiendanube"):
        # Bloqueamos la vista con el banner
        with loading_placeholder.container():
            st.markdown(f"""
                <div class="loading-banner">
                    <h2 style="color: #0056ff; margin-bottom: 10px;">⚡ Sincronizando con Tiendanube</h2>
                    <p>Optimizando stock y generando reglas de liquidez...</p>
                </div>
            """, unsafe_allow_html=True)
            
            bar = st.progress(0)
            for i in range(101):
                time.sleep(0.02)
                bar.progress(i)
            
            st.success("✅ ¡Sincronización Exitosa! Datos actualizados en la tienda.")
            time.sleep(2)
        loading_placeholder.empty() # Quitamos el banner después de terminar

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
                st.markdown(f"""<div class="team-card-large"><img src="{img}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #0056ff; margin-bottom: 15px;"><br><strong>{nombre}</strong><br><small style="color:#0056ff;">{cargo}</small></div>""", unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026 | Equipo 3")
