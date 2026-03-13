import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import os
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURACIÓN Y SEGURIDAD ---
st.set_page_config(page_title="Flowmerce IA - Liquidez", page_icon="🌊", layout="wide")

# Mejora Seguridad: Intenta usar secrets, si no, usa el hardcoded por ahora (Hackathon mode)
CLIENT_ID = st.secrets.get("CLIENT_ID", "27483")
CLIENT_SECRET = st.secrets.get("CLIENT_SECRET", "d45072c95b889632ad3040bfd1dd951d981e0c38ff25877a")

# --- 2. LÓGICA DE NEGOCIO (Movida arriba para mejor arquitectura) ---
def determinar_accion_ia(row, lead_time):
    # Lógica de IA: Safety Stock (Punto 4 de la revisión)
    # Si el stock es menor al stock de seguridad (ventas durante lead time + 50% de reserva)
    safety_stock = row["V_Diaria"] * lead_time * 1.5
    
    if row["Stock"] < safety_stock:
        return "🚨 REABASTECER (Stock Crítico)"
    elif row["Autonomia"] > 60:
        return "🔥 LIQUIDAR (Exceso de Capital)"
    return "✅ ÓPTIMO"

def obtener_token_real(code):
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {"client_id": int(CLIENT_ID), "client_secret": CLIENT_SECRET, "grant_type": "authorization_code", "code": code.strip()}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("access_token") if response.status_code == 200 else None
    except requests.RequestException:
        return None

# --- 3. DICCIONARIO MULTILINGÜE ---
textos = {
    "Español": {"sub": "Convierte Inventario en Flujo de Efectivo", "tab1": "📊 Dashboard", "tab2": "🧠 Estrategia IA", "tab3": "👥 Equipo"},
    "Português": {"sub": "Converta Estoque em Fluxo de Caixa", "tab1": "📊 Dashboard", "tab2": "🧠 Estratégia IA", "tab3": "👥 Equipe"},
    "English": {"sub": "Turn Inventory into Cash Flow", "tab1": "📊 Dashboard", "tab2": "🧠 AI Strategy", "tab3": "👥 Team"}
}

# --- 4. GESTIÓN DE MEMORIA ---
if 'db_inventario' not in st.session_state:
    st.session_state.db_inventario = pd.DataFrame({
        "Producto": ["Tenis Pro Runner", "Gorra Blue Urban", "Calcetín Sport", "Sudadera Lino"],
        "Stock": [15, 95, 45, 4],
        "Ventas_30d": [45, 10, 30, 42],
        "Costo": [1200, 350, 150, 890]
    })

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg", use_container_width=True)
    
    with st.expander("🌐 Accesibilidad", expanded=False):
        idioma = st.selectbox("Idioma", ["Español", "Português", "English"])
        lectura_facil = st.toggle("Modo Lectura Fácil")
        alto_contraste = st.toggle("Alto Contraste")

    st.markdown("### ⚙️ Simulador Pro")
    f_demanda = st.slider("Impulso de Demanda", 0.5, 4.0, 1.0)
    dias_entrega = st.slider("Lead Time (Días)", 1, 30, 7)
    
    # Persistencia de Token (Punto 2 de la revisión)
    if "token_tienda" in st.session_state:
        st.success("Tienda Conectada ✅")
    else:
        with st.expander("🔑 Conexión Tiendanube", expanded=True):
            # Scope ampliado (Punto 3 de la revisión)
            scope = "read_products,write_products,read_orders,write_orders"
            st.link_button("Autorizar", f"https://www.tiendanube.com/apps/authorize?client_id={CLIENT_ID}&scope={scope}")
            temp_code = st.text_input("Code:")
            if st.button("Vincular"):
                token = obtener_token_real(temp_code)
                if token:
                    st.session_state.token_tienda = token
                    st.rerun()

# --- 6. CÁLCULOS VECTORIZADOS ---
t_act = textos[idioma]
df = st.session_state.db_inventario.copy()
df["V_Diaria"] = (df["Ventas_30d"] / 30) * f_demanda
df["Autonomia"] = np.where(df["V_Diaria"] > 0, df["Stock"] / df["V_Diaria"], np.nan)
df["Capital_Total"] = df["Stock"] * df["Costo"]

# Métricas Wow (Punto Feature WOW)
capital_total_sum = df["Capital_Total"].sum()
filtro_liberable = df["Autonomia"] > 60
capital_liberable = df.loc[filtro_liberable, "Capital_Total"].sum()
indice_liberacion = (capital_liberable / capital_total_sum) if capital_total_sum > 0 else 0

# --- 7. UI Y ESTILOS ---
extra_styles = f"html, body {{ font-size: 1.2rem; }}" if lectura_facil else ""
if alto_contraste: extra_styles += ".stApp { background: #000 !important; color: #fff !important; }"

st.markdown(f"<style>{extra_styles} .main-title {{ background: linear-gradient(90deg, #0056ff, #00c6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem !important; font-weight: 800; text-align: center; }} </style>", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌊 Flowmerce IA</h1>', unsafe_allow_html=True)
st.subheader(f"✨ {t_act['sub']}")

# --- 8. DASHBOARD ---
tab1, tab2, tab3 = st.tabs([t_act["tab1"], t_act["tab2"], t_act["tab3"]])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Capital Atrapado", f"${capital_liberable:,.0f}")
    c2.metric("Ventas en Riesgo", f"${df[df['Autonomia'] < dias_entrega]['Capital_Total'].sum() * 1.5:,.0f}")
    # Feature WOW: Cash Liberation Index
    c3.metric("⚡ Cash Liberation Index", f"{indice_liberacion*100:.1f}%", help="Porcentaje de tu capital que puedes liberar hoy optimizando stock.")
    c4.metric("Salud de Inventario", f"{100 - (indice_liberacion*100):.1f}%")

    st.write("---")
    # Gráfico Real (Punto 5 de la revisión)
    st.subheader("💰 Distribución de Capital por Producto")
    st.bar_chart(df.set_index("Producto")["Capital_Total"])

with tab2:
    st.subheader("🤖 Recomendaciones de IA Estratégica")
    df["Acción Sugerida"] = df.apply(lambda x: determinar_accion_ia(x, dias_entrega), axis=1)
    
    # Tabla con UX mejorada
    st.dataframe(df[["Producto", "Stock", "Autonomia", "Acción Sugerida"]].style.highlight_max(axis=0, subset=["Autonomia"]), use_container_width=True)
    
    if st.button("🚀 Aplicar Cambios en Tiendanube"):
        with st.status("Optimizando tienda..."): time.sleep(2)
        st.balloons()

with tab3:
    st.markdown("### 👥 Equipo 3")
    # (Aquí va tu bloque de integrantes que ya tienes, se mantiene igual)
    equipo = [("Willan Á.", "Lead Architect", "https://i.imgur.com/CSH9Af7.jpeg"), ("Dalia R.", "Product Manager", "https://i.imgur.com/4O2BGL8.jpeg")]
    cols = st.columns(2)
    for i, (n, c, img) in enumerate(equipo):
        with cols[i]: st.image(img, width=100); st.write(f"**{n}**\n{c}")

st.divider()
st.caption("🌊 Flowmerce IA | Hackathon UTEL 2026")
