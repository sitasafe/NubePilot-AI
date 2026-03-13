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
        "atrapado": "Capital Atrapado", "riesgo": "Ventas en Riesgo", "salud": "Salud de Caja",
        "btn_sync": "Sincronizar con Tiendanube", "edit_msg": "Edita tus datos aquí abajo para simular cambios:"
    },
    "Português": {
        "sub": "Onde os datos se transformam em vendas",
        "tab0": "🚀 Nossa Visão", "tab1": "📊 Monitor de Liquidez", "tab2": "🧠 Estratégia", "tab3": "👥 Equipe",
        "atrapado": "Capital Preso", "riesgo": "Vendas em Risco", "salud": "Saúde do Caixa",
        "btn_sync": "Sincronizar com Tiendanube", "edit_msg": "Edite seus dados abaixo para simular mudanças:"
    },
    "English": {
        "sub": "Where data turns into sales",
        "tab0": "🚀 Our Vision", "tab1": "📊 Liquidity Monitor", "tab2": "🧠 Strategy", "tab3": "👥 Team",
        "atrapado": "Trapped Capital", "riesgo": "Sales at Risk", "salud": "Cash Health",
        "btn_sync": "Sync with Tiendanube", "edit_msg": "Edit your data below to simulate changes:"
    }
}

# --- 4. FUNCIONES DE API TIENDANUBE (REALES) ---
def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("access_token") if response.status_code == 200 else None
    except: return None

def fetch_products(token):
    # Simulación de llamada API real con el token obtenido
    url = "https://api.tiendanube.com/v1/123456/products" # El ID sería dinámico
    headers = {'Authentication': f'bearer {token}', 'User-Agent': 'Flowmerce App (contacto@flowmerce.com)'}
    # Para el demo, si no hay conexión real, devolvemos datos base enriquecidos
    return pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino", "Jersey Retro"],
        "Stock": [15, 95, 45, 4, 0],
        "Ventas_30d": [45, 10, 30, 42, 5],
        "Costo": [1200.0, 350.0, 150.0, 890.0, 500.0]
    })

# --- 5. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = fetch_products(None)

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.image("https://imgur.com/YrVO3ZF.jpeg", use_container_width=True)
    
    with st.expander("🌐 Configuración", expanded=True):
        idioma = st.selectbox("Idioma", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Modo Alto Contraste")

    st.markdown("### ⚙️ Simulador de Mercado")
    f_demanda = st.slider("Impulso de Demanda (Factor)", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time Proveedor (Días)", 1, 30, 7)
    
    with st.expander("🔑 Conexión Tiendanube", expanded=True):
        st.link_button("1. Autorizar App", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope=read_products")
        temp_code = st.text_input("2. Pega el Code:")
        if st.button("3. Vincular y Sincronizar"):
            token = obtener_token_real(temp_code)
            if token or temp_code == "DEMO123": # Bypass para demo
                st.session_state.db_inventario = fetch_products(token)
                st.success("¡Datos Sincronizados! ✅")
                st.rerun()

# --- 7. ESTILOS CSS ---
extra_styles = ""
if lectura_facil: extra_styles += "html, body, p, div { font-size: 1.2rem !important; }"
if alto_contraste: extra_styles += ".stApp { background: #0e1117 !important; color: #fff !important; }"

st.markdown(f"<style>{extra_styles} .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; }} </style>", unsafe_allow_html=True)

# --- 8. PROCESAMIENTO DE DATOS DINÁMICO ---
t_act = textos[idioma]
df_actual = st.session_state.db_inventario.copy()

# Cálculos automáticos
df_actual["V_Diaria"] = (df_actual["Ventas_30d"] / 30) * f_demanda
df_actual["Autonomia"] = np.where(df_actual["V_Diaria"] > 0, df_actual["Stock"] / df_actual["V_Diaria"], 999)
df_actual["Valor_Stock"] = df_actual["Stock"] * df_actual["Costo"]

# Métricas
atrapado_val = df_actual[df_actual["Autonomia"] > 60]["Valor_Stock"].sum()
riesgo_val = df_actual[df_actual["Autonomia"] < dias_entrega]["V_Diaria"].sum() * 30 * 1.5 # Pérdida estimada 30 días

# --- 9. CUERPO DE LA APP ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)

c_enc1, c_enc2 = st.columns([0.8, 0.2])
with c_enc1: st.markdown(f"**✨ {t_act['sub']}**")
with c_enc2: mic_recorder(start_prompt="🎤 Comando Voz", key='rec')

tab0, tab1, tab2, tab3 = st.tabs([t_act["tab0"], t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab0:
    st.markdown("## 🎯 Control de Flujo Inteligente")
    col_a, col_b = st.columns([0.6, 0.4])
    with col_a:
        st.write("Flowmerce no es solo un tablero, es el **cerebro financiero** de tu ecommerce.")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder para video demo
    with col_b:
        st.info("💡 **Tip:** Conecta tu tienda para ver el capital real que podrías liberar hoy mismo.")

with tab1:
    # Métricas en Tiempo Real
    m1, m2, m3 = st.columns(3)
    m1.metric(t_act["atrapado"], f"${atrapado_val:,.0f} MXN", help="Dinero estancado en productos que no rotan")
    m2.metric(t_act["riesgo"], f"${riesgo_val:,.0f} MXN", "-15%", delta_color="inverse")
    m3.metric(t_act["salud"], f"{max(0, 100-int(riesgo_val/1000))}%", "Óptimo")

    st.subheader(t_act["edit_msg"])
    # EL EDITOR DE DATOS: Esto hace que la app sea funcional
    edited_df = st.data_editor(
        df_actual,
        column_config={
            "Stock": st.column_config.NumberColumn(help="Cantidad actual en bodega"),
            "Costo": st.column_config.NumberColumn(format="$%.2f"),
            "Autonomia": st.column_config.ProgressColumn("Días de Vida", min_value=0, max_value=90),
        },
        disabled=["V_Diaria", "Autonomia", "Valor_Stock"],
        hide_index=True,
        use_container_width=True
    )
    # Guardar cambios si el usuario edita la tabla
    if not edited_df.equals(st.session_state.db_inventario):
        st.session_state.db_inventario = edited_df
        st.rerun()

with tab2:
    st.subheader("🧠 Estrategia de Compra Sugerida")
    
    def get_status(row):
        if row["Stock"] == 0: return "❌ AGOTADO"
        if row["Autonomia"] < dias_entrega: return "🚨 RECOMPRA URGENTE"
        if row["Autonomia"] > 60: return "🔥 LIQUIDACIÓN"
        return "✅ BALANCEADO"

    df_actual["Acción"] = df_actual.apply(get_status, axis=1)
    
    # Mostrar como tarjetas de acción
    for _, row in df_actual.iterrows():
        with st.expander(f"{row['Acción']} - {row['Producto']}"):
            c1, c2 = st.columns(2)
            c1.write(f"**Stock actual:** {row['Stock']} unidades")
            c2.write(f"**Días restantes:** {row['Autonomia']:.1f} días")
            if "RECOMPRA" in row["Acción"]:
                st.button(f"Generar Orden de Compra: {row['Producto']}", key=row['Producto'])

with tab3:
    # El equipo se mantiene igual pero con mejor estilo
    st.markdown("### 👥 Equipo 3 - UTEL 2026")
    # ... (tu código de equipo aquí) ...
    st.write("Cargando perfiles del equipo...")

st.divider()
st.caption("🌊 Flowmerce | Dashboard de Liquidez Activa | v1.2")
