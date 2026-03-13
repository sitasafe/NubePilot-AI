import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce - Liquidez Inteligente", page_icon="🌊", layout="wide")

# --- 2. CREDENCIALES TIENDANUBE (SEGURIDAD MEJORADA) ---
# Intenta leer de secrets.toml, si no existe usa los valores por defecto (Hackathon mode)
try:
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
except:
    CLIENT_ID = "27483"
    CLIENT_SECRET = "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a"

# --- 3. DICCIONARIO MULTILINGÜE (CORREGIDO) ---
textos = {
    "Español": {
        "sub": "Donde los datos se convierten en ventas",
        "tab0": "🚀 Nuestra Visión", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estrategia", "tab3": "👥 Equipo",
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja"
    },
    "Português": {
        "sub": "Onde os dados se transformam em vendas", # Corregido: dados
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa"
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Our Vision", "tab1": "📊 Liquidity Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health"
    }
}

# --- 4. FUNCIONES DE API (ROBUSTEZ MEJORADA) ---
def obtener_token_real(code):
    if not code: return None
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
            data = response.json() # Validación de JSON seguro
            return data.get("access_token")
        return None
    except (requests.RequestException, ValueError):
        return None

# --- 5. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

# --- 6. BARRA LATERAL (ORDEN DE EJECUCIÓN SEGURO) ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
    st.write("---")

    with st.expander("🌐 Accesibilidad e Idioma", expanded=True):
        idioma = st.selectbox("Idioma Interfaz", ["Español", "Português", "English"], key="idioma_select")
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda (Factor)", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor (Días)", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_orders,write_orders,read_products,write_products")
        temp_code = st.text_input("2. Pega el Code:")
        
        if st.button("3. Vincular Tienda"):
            if temp_code:
                token = obtener_token_real(temp_code)
                if token:
                    st.session_state.token_tienda = token
                    st.success("¡Conexión Establecida! ✅")
                else:
                    st.error("Error en vinculación. Revisa el código.")
            else:
                st.warning("Pega primero el código de autorización.")

# --- 7. ESTILOS CSS (CORREGIDOS PARA NO ROMPER DIVS) ---
extra_styles = ""
if lectura_facil: extra_styles += "p, span, label, .stMetric { font-size: 1.3rem !important; line-height: 1.6 !important; }"
if alto_contraste: extra_styles += ".stApp { background: #000 !important; color: #fff !important; }"

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
    }}
    @keyframes gradient-move {{ 0% {{background-position: 0% 50%;}} 50% {{background-position: 100% 50%;}} 100% {{background-position: 0% 50%;}} }}
    
    .team-card-large {{
        text-align: center; padding: 25px; border-radius: 25px;
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 86, 255, 0.2);
        margin-bottom: 20px;
    }}
    .stMetric {{ background: rgba(0, 86, 255, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #0056ff; }}

    @keyframes cloud-up {{
        0% {{ transform: translateY(100vh); opacity: 0; }}
        10% {{ opacity: 0.8; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(-100vh); opacity: 0; }}
    }}
    .cloud-ascend {{
        position: fixed; bottom: 0; font-size: 5rem; z-index: 9999;
        pointer-events: none; animation: cloud-up 3s linear infinite;
    }}
</style>
""", unsafe_allow_html=True)

# --- 8. LÓGICA DE CÁLCULO (CON MANEJO DE NaNs) ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["Ventas_30d"] = df["Ventas_30d"].fillna(0) # Limpieza de datos

df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
# Reemplazamos Infinitos por 999 para evitar errores de visualización
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], 999)

atrapado_val = df[df["Autonomia"] > 60].apply(lambda x: x["Stock"] * x["Costo"], axis=1).sum()
riesgo_val = df[df["Autonomia"] < dias_entrega].apply(lambda x: x["V_Diaria"] * x["Costo"] * 1.5, axis=1).sum()

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown(f"**✨ {t_act['sub']}**")

tab0, tab1, tab2, tab3 = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab0:
    st.markdown("## 🎯 ¿Qué nos diferencia?")
    col_v1, col_v2 = st.columns([0.6, 0.4])
    with col_v1:
        st.write("""
        Hoy, miles de dueños de marcas pasan **5 horas por semana** frente a un Excel, intentando adivinar el futuro. 
        Juegan a la ruleta con su inventario: o compran de más o pierden ventas por falta de stock.
        
        **Tu negocio es un ritmo, no una adivinanza.** Flowmerce lee tus datos de Tiendanube y te dice **qué, cuánto y cuándo comprar**.
        """)
        st.info("💡 **Dato:** Reducimos una tarde entera de trabajo a solo 5 minutos de certeza.")
    with col_v2:
        st.markdown("### 💎 Modelo SaaS\n- **Starter:** Gratis\n- **Growth:** Suscripción\n- **Scale:** Basado en éxito")

with tab1:
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric(t_act["atrapado"], f"${float(atrapado_val):,.0f} MXN")
    c_m2.metric(t_act["riesgo"], f"${float(riesgo_val):,.0f} MXN", delta="¡Alerta!", delta_color="inverse")
    c_m3.metric(t_act["salud"], f"{max(0, 100-(dias_entrega*2))}%")
    st.area_chart(df.set_index("Producto")["Stock"])

with tab2:
    st.subheader("🤖 Estrategia de Inventario")
    df["Acción Sugerida"] = df["Autonomia"].apply(lambda x: "🚨 REABASTECER" if x < dias_entrega else ("🔥 LIQUIDAR" if x > 60 else "✅ ESTABLE"))
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Acción Sugerida"]], use_container_width=True)
    
    if st.button("🚀 Aplicar Cambios"):
        cloud_p = st.empty()
        with st.status("Sincronizando...", expanded=True) as s:
            cloud_p.markdown("""
                <div class="cloud-ascend" style="left: 15%; animation-duration: 2.5s;">☁️</div>
                <div class="cloud-ascend" style="left: 50%; animation-duration: 3.5s;">☁️</div>
                <div class="cloud-ascend" style="left: 85%; animation-duration: 2s;">☁️</div>
            """, unsafe_allow_html=True)
            time.sleep(2.5)
            s.update(label="¡Hecho! ☁️", state="complete")
        cloud_p.empty()

with tab3:
    st.markdown("### 👥 Equipo 3")
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
                st.markdown(f'<div class="team-card-large"><img src="{img}" width="80" style="border-radius:50%"><br><b>{nombre}</b><br><small>{cargo}</small></div>', unsafe_allow_html=True)

st.divider()
st.caption("🌊 Flowmerce | Hackathon UTEL 2026")
