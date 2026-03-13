import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Inteligencia de Capital", page_icon="🌊", layout="wide")

# --- 2. CREDENCIALES Y CONSTANTES ---
CLIENT_ID = "27483"
CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- 3. DICCIONARIO MULTILINGÜE ---
textos = {
    "Español": {
        "sub": "De inventario estancado a flujo de efectivo inteligente",
        "tab1": "📊 Dashboard de Liquidez", "tab2": "🤖 Decisiones IA", "tab3": "👥 Equipo",
        "atrapado": "Dinero Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Inventario"
    },
    "Português": {
        "sub": "De estoque estagnado a fluxo de caixa inteligente",
        "tab1": "📊 Dashboard de Liquidez", "tab2": "🤖 Decisões IA", "tab3": "👥 Equipe",
        "atrapado": "Dinheiro Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Estoque"
    },
    "English": {
        "sub": "From stagnant inventory to smart cash flow",
        "tab1": "📊 Liquidity Dashboard", "tab2": "🤖 AI Decisions", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Inventory Health"
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

# --- 5. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

# --- 6. BARRA LATERAL (PANEL DE CONTROL AVANZADO) ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    
    with st.expander("🌐 Accesibilidad e Idioma", expanded=False):
        idioma = st.selectbox("Idioma", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Alto Contraste")

    st.header("⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time (Días de entrega)", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.info("ID Tienda: 2831942")
        temp_code = st.text_input("Pega el Code de Autorización:")
        if st.button("Vincular con Flowmerce"):
            token = obtener_token_real(temp_code)
            if token: st.success("¡Conectado! ✅")
            else: st.warning("Usando modo demostración.")

    st.divider()
    st.markdown("### 📲 Notificaciones")
    st.toggle("Plan del día a WhatsApp", value=True)
    st.toggle("Alertas SMS (Zonas rurales)", value=False)

# --- 7. ESTILOS DINÁMICOS (CSS INTEGRADO) ---
extra_css = ""
if lectura_facil: extra_css += "html, body, p, div { font-size: 1.3rem !important; }"
if alto_contraste: extra_css += ".stApp { background-color: #000; color: #fff; } .team-card { border: 1px solid white !important; }"

st.markdown(f"""
<style>
    {extra_css}
    .main-title {{
        background: linear-gradient(90deg, #0056ff, #00c6ff, #6200ea);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; font-weight: 800; text-align: center;
    }}
    .team-card {{
        text-align: center; padding: 20px; border-radius: 20px;
        background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(0, 86, 255, 0.2);
        transition: 0.3s; margin-bottom: 15px;
    }}
    .team-card:hover {{ transform: translateY(-10px); border-color: #0056ff; }}
    .team-img {{ width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #0056ff; }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE NEGOCIO ---
t = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = df["Stock"] / df["V_Diaria"]

atrapado_val = df[df["Autonomia"] > 60].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()
riesgo_val = df[df["Autonomia"] < dias_entrega].apply(lambda x: x["V_Diaria"] * x["Costo"] * 1.5, axis=1).sum()

# --- 9. INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="main-title">🚀 Flowmerce IA</h1>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>{t['sub']}</p>", unsafe_allow_html=True)

# Integración de Voz
c_voz1, c_voz2 = st.columns([0.8, 0.2])
with c_voz2:
    audio = mic_recorder(start_prompt="🎤 Comando de Voz", stop_prompt="🛑 Parar", key='rec')

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric(t["atrapado"], f"${atrapado_val:,.2f}")
    c2.metric(t["riesgo"], f"${riesgo_val:,.2f}", delta="Crítico", delta_color="inverse")
    c3.metric(t["salud"], f"{max(0, 100-(dias_entrega*2))}%")
    
    st.subheader("📈 Proyección de Liquidez 2026")
    st.area_chart(np.random.randn(20, 1) * 1000 + 5000)
    st.info("💡 **Insight:** El 60% de tus ventas vendrán de dispositivos móviles en zonas de baja red. Flowmerce optimizó tu caché.")

with tab2:
    st.subheader("⚡ Acciones Sugeridas por IA")
    def sugerir(fila):
        if fila["Autonomia"] < dias_entrega: return "🚨 COMPRAR URGENTE"
        if fila["Autonomia"] > 60: return "🔥 LIQUIDAR STOCK"
        return "✅ ESTABLE"
    
    df["Accion"] = df.apply(sugerir, axis=1)
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Accion"]], use_container_width=True)
    
    if st.button("🚀 Aplicar Estrategia en Tiendanube"):
        with st.status("Sincronizando..."):
            time.sleep(2)
        st.balloons()
        st.success("Precios actualizados y órdenes de compra enviadas.")

with tab3:
    st.markdown("### 👥 Equipo 3 - Flowmerce")
    equipo = [
        ("Willan Á.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"),
        ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg"),
        ("Montserrat G.", "Strategy", "https://cdn-icons-png.flaticon.com/512/6997/6997674.png"),
        ("Jiram C.", "Organization", "https://i.imgur.com/eamMDmE.jpeg"),
        ("Carlos A.", "Leadership", "https://cdn-icons-png.flaticon.com/512/2354/2354573.png"),
        ("Edwing G.", "Sales", "https://i.imgur.com/CQJu9xm.jpeg"),
        ("Amarilis E.", "Management", "https://cdn-icons-png.flaticon.com/512/201/201634.png"),
        ("César F.", "Strategy", "https://cdn-icons-png.flaticon.com/512/3001/3001764.png")
    ]
    
    cols = st.columns(4)
    for i, (nombre, cargo, img) in enumerate(equipo):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="team-card">
                <img src="{img}" class="team-img">
                <p><strong>{nombre}</strong><br><small>{cargo}</small></p>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("Flowmerce v4.0 | Equipo 3 | Hackathon UTEL 2026 | Tiendanube Partner")
