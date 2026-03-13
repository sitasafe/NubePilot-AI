with tabs[2]:
    st.subheader(t_act["est_tit"])
    
    # --- SIMULADOR DE ESCENARIOS ---
    with st.expander(t_act["sim_tit"], expanded=False):
        sim_inv = st.number_input(t_act["sim_inv"], value=50000)
        c_s1, c_s2 = st.columns(2)
        with c_s1: st.markdown(f'<div style="background: linear-gradient(135deg, #0056ff 0%, #6200ea 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;"><small>{t_act["sim_proj"]}</small><h3>${sim_inv * (f_demanda * 1.8):,.0f} MXN</h3></div>', unsafe_allow_html=True)
        with c_s2: st.markdown(f'<div style="background: linear-gradient(135deg, #00c6ff 0%, #0056ff 100%); color: white; padding: 25px; border-radius: 15px; text-align: center;"><small>{t_act["sim_rec"]}</small><h3>{30/f_demanda:.1f} {t_act["sim_dias"]}</h3></div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # --- TABLA INTERACTIVA (DATA EDITOR) ---
    st.markdown("### 📝 Gestión Dinámica de Inventario")
    st.caption("Modifica los valores directamente en la tabla para simular cambios de stock o ventas.")
    
    # Pre-calculamos las acciones para mostrar colores
    def determinar_accion(row):
        autonomia = (row["Stock"] / ((row["Ventas_30d"] / 30) * f_demanda)) if row["Ventas_30d"] > 0 else 999
        if autonomia < dias_entrega: return "🚨 REABASTECER"
        if autonomia > 60: return "🔥 LIQUIDAR"
        return "✅ ESTABLE"

    # Mostramos el editor de datos
    df_editable = st.data_editor(
        st.session_state.db_inventario,
        column_config={
            "Producto": st.column_config.TextColumn("Producto", disabled=True),
            "Stock": st.column_config.NumberColumn("Stock Actual", min_value=0, step=1),
            "Ventas_30d": st.column_config.NumberColumn("Ventas (30 días)", min_value=0, step=1),
            "Costo": st.column_config.CurrencyColumn("Costo Unitario", currency="MXN"),
        },
        hide_index=True,
        use_container_width=True,
        key="editor_inventario"
    )

    # Si el usuario cambia algo, actualizamos el estado global
    if not df_editable.equals(st.session_state.db_inventario):
        st.session_state.db_inventario = df_editable
        st.rerun() # Refresca todo el dashboard con los nuevos datos

    # --- BOTONES DE ACCIÓN ---
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button(t_act["btn_app"], use_container_width=True):
            animar_nubes()
            st.success("📦 Pedidos de reabastecimiento enviados a Tiendanube")
    
    with col_b2:
        csv = df_editable.to_csv(index=False).encode('utf-8')
        st.download_button(label=t_act["btn_reporte"], data=csv, file_name='Plan_Accion_Flowmerce.csv', use_container_width=True)
