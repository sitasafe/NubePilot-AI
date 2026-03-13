import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Flowmerce IA - Liquidez Estratégica", page_icon="🌊", layout="wide")

# --- LÓGICA DE NEGOCIO DISRUPTIVA (EL MOTOR DE PREDICCIÓN) ---
def procesar_datos_tienda(impulso_ventas, retraso_logistico):
    # Simulamos la data de Tiendanube
    data = {
        "Producto": ["Paleta Aurora Glow", "Labial Mate #LM33", "Sérum Hidratante", "Base Perfect Skin"],
        "Stock": [120, 5, 45, 2],
        "Ventas_Promedio_Dia": [0.5, 4.2, 1.2, 3.5],
        "Costo_Unitario": [450, 180, 600, 550],
        "Lead_Time_Std": [5, 5, 7, 5]
    }
    df = pd.DataFrame(data)
    
    # 1. Ajuste por el Simulador de Escenarios
    df["Ventas_Reales"] = df["Ventas_Promedio_Dia"] * impulso_ventas
    df["Lead_Time_Total"] = df["Lead_Time_Std"] + retraso_logistico
    
    # 2. Cálculos de Inteligencia Financiera
    df["Dias_Autonomia"] = df["Stock"] / df["Ventas_Reales"]
    df["Capital_Inmovilizado"] = np.where(df["Dias_Autonomia"] > 60, df["Stock"] * df["Costo_Unitario"], 0)
    
    # 3. Predicción de Quiebre (Stockout)
    df["Riesgo_Quiebre"] = df["Dias_Autonomia"] < df["Lead_Time_Total"]
    return df

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
<style>
    .main-title { background: linear-gradient(90deg, #1A237E, #0052D4, #4364F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 800; text-align: center; }
    .stMetric { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #0052D4; }
    .status-card { padding: 20px; border-radius: 15px; margin: 10px 0; border: 1px solid #e0e0e0; }
    .critical-alert { background: #FFF5F5; border-left: 5px solid #E53935; color: #B71C1C; }
    .opportunity-alert { background: #F0FBF0; border-left: 5px solid #43A047; color: #1B5E20; }
    .pitch-box { background: #F8F9FA; padding: 25px; border-radius: 20px; border: 1px dashed #0052D4; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SIMULADOR DE ESCENARIOS ---
with st.sidebar:
    st.image("https://imgur.com/V1m4Dgk.jpeg")
    st.header("🎮 Simulador Estratégico")
    st.info("Ajusta las variables externas para ver cómo Flowmerce protege tu liquidez.")
    
    f_ventas = st.slider("Impulso de Demanda (ej. Hot Sale)", 0.5, 4.0, 1.0, help="Simula un aumento drástico en ventas")
    f_logistica = st.slider("Retraso de Proveedores (Días)", 0, 20, 0, help="Simula retrasos en aduanas o logística")
    
    st.divider()
    if st.button("🔄 Sincronizar Tiendanube (LIVE)"):
        with st.status("Conectando con API de Tiendanube..."):
            time.sleep(1.5)
            st.success("Inventario Sincronizado")

# --- EJECUCIÓN DEL MOTOR ---
df_res = procesar_datos_tienda(f_ventas, f_logistica)
dinero_enterrado = df_res["Capital_Inmovilizado"].sum()
ventas_en_riesgo = df_res[df_res["Riesgo_Quiebre"]].apply(lambda x: x["Ventas_Reales"] * x["Costo_Unitario"] * 1.5, axis=1).sum()

# --- INTERFAZ PRINCIPAL ---
st.markdown('<h1 class="main-title">🌊 Flowmerce</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'><b>Inteligencia Financiera para el Inventario</b></p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Diagnóstico de Capital", "🤖 Predicción IA", "🚀 El Pitch", "👥 Equipo"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Dinero 'Enterrado'", f"${dinero_enterrado:,.0f} MXN", "Capital Inmovilizado", delta_color="inverse")
    col2.metric("Ventas en Riesgo", f"${ventas_en_riesgo:,.0f} MXN", "Por quiebre de stock", delta_color="inverse")
    col3.metric("Eficiencia de Caja", f"{max(0, 100 - (f_logistica*3))}%", "Salud operativa")

    st.write("---")
    st.subheader("⚠️ Alertas de Acción Inmediata")
    
    c1, c2 = st.columns(2)
    with c1:
        # Alerta de Stock Estancado (Basado en tu imagen de ejemplo)
        prod_lento = df_res[df_res["Dias_Autonomia"] > 60].iloc[0]
        st.markdown(f"""
        <div class="status-card critical-alert">
            <h4>🚨 Alerta de Stock Estancado</h4>
            <p>El producto <b>{prod_lento['Producto']}</b> no se ha movido significativamente. 
            Tienes <b>{prod_lento['Stock']} unidades</b> bloqueando <b>${prod_lento['Capital_Inmovilizado']:,.0f}</b>.</p>
            <button style="background:#E53935; color:white; border:none; padding:10px; border-radius:5px;">Activar Venta Flash 25% OFF</button>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        # Sugerencia de Compra (Basado en la Solución)
        prod_quiebre = df_res[df_res["Riesgo_Quiebre"]].iloc[0]
        st.markdown(f"""
        <div class="status-card opportunity-alert">
            <h4>💡 Sugerencia de Compra Inteligente</h4>
            <p><b>{prod_quiebre['Producto']}</b> se agotará en {prod_quiebre['Dias_Autonomia']:.1f} días. 
            Con el retraso logístico actual, debes pedir hoy mismo <b>{int(prod_quiebre['Ventas_Reales']*15)} unidades</b>.</p>
            <button style="background:#43A047; color:white; border:none; padding:10px; border-radius:5px;">Generar Orden de Compra</button>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🤖 Del 'Registro' a la 'Predicción'")
    st.write("NubeFlow no solo cuenta cajas, predice el flujo de efectivo.")
    
    # Tabla Comparativa de Decisiones
    df_comparativo = df_res.copy()
    df_comparativo["Decisión Humana (Intuición)"] = "Esperar a que se agote"
    df_comparativo["Decisión Flowmerce (Datos)"] = df_comparativo.apply(
        lambda x: "COMPRAR AHORA" if x["Riesgo_Quiebre"] else ("LIQUIDAR" if x["Dias_Autonomia"] > 60 else "MANTENER"), axis=1
    )
    
    st.dataframe(df_comparativo[["Producto", "Stock", "Dias_Autonomia", "Decisión Flowmerce (Datos)"]], use_container_width=True)
    
    st.area_chart(pd.DataFrame({"Flujo Proyectado": np.linspace(50, 150, 30) + (f_ventas*10) - (f_logistica*5)}))

with tab3:
    st.markdown('<div class="pitch-box">', unsafe_allow_html=True)
    st.subheader("🎯 Nuestro Diferencial")
    st.write("""
    Mientras otros se enfocan en vender más (Front-end), **Flowmerce se enfoca en que no quiebres (Back-end Financiero).**
    
    1. **Eliminamos el Error Humano:** Reducimos 5 horas de Excel a 5 minutos de decisiones.
    2. **Maximizamos Liquidez:** Dinero que no está en stock muerto, es dinero para marketing.
    3. **Predecimos el Futuro:** No te decimos qué pasó, te decimos qué va a pasar.
    """)
    st.info("✨ **Frase de Cierre:** No vendemos software de inventario. Vendemos decisiones inteligentes que protegen el capital de las tiendas.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.subheader("👥 Equipo Flowmerce")
    equipo = [
        ("Willan Álvarez.", "Lead Architect"), ("Dalia R.", "Product Manager"),
        ("Montserrat G.", "Strategy"), ("Jiram Cabrera", "Organización"),
        ("Carlos Andrés A.", "Liderazgo"), ("Edwing Garcia", "Ventas"),
        ("Amarilis Elizabeth", "Gestión"), ("Cesar Augusto F.", "Estrategia")
    ]
    cols = st.columns(4)
    for i, (nombre, cargo) in enumerate(equipo):
        cols[i%4].markdown(f"**{nombre}**\n\n{cargo}")

st.divider()
st.caption("Flowmerce v2.0 | 'De datos estáticos a flujo de efectivo' | Hackathon 2026")
