import streamlit as st
import streamlit.components.v1 as components


def disparar_alerta_critica(productos):
    if productos is None or len(productos) == 0:
        return False, "Sin productos críticos."

    if hasattr(productos, "sort_values"):
        top = productos.sort_values("Autonomia").iloc[0]
        nombre = str(top.get("Producto", "Producto crítico"))
        autonomia = float(top.get("Autonomia", 0))
    else:
        top = productos[0]
        nombre = str(top.get("Producto", "Producto crítico"))
        autonomia = float(top.get("Autonomia", 0))

    # Short alert sound for demo "wow effect".
    components.html(
        """
        <audio autoplay>
          <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
        </audio>
        """,
        height=0,
    )

    mensaje = (
        f"🚨 ALERTA DE LIQUIDEZ: {nombre} se agotará en menos de {autonomia:.1f} días"
    )
    return True, mensaje
