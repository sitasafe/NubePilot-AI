import asyncio
import re

import pandas as pd
import requests
import streamlit as st

from app.core.state import get_http_session, obtener_token_seguro


def normalizar_store_id(raw_store_id):
    if raw_store_id is None:
        return ""
    text = str(raw_store_id).strip()
    if not text:
        return ""
    match = re.search(r"/(\d+)(?:/|$)", text)
    if match:
        return match.group(1)
    only_digits = re.sub(r"\D", "", text)
    return only_digits if only_digits else ""


def obtener_token_real(code, client_id, client_secret):
    if not code or not client_secret:
        return None
    url = "https://www.tiendanube.com/apps/authorize/token"
    payload = {
        "client_id": int(client_id),
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code.strip(),
    }
    try:
        response = get_http_session().post(url, json=payload, timeout=10)
        if response.status_code != 200:
            return None
        body = response.json()
        return {
            "access_token": body.get("access_token"),
            "store_id": str(body.get("user_id", "")).strip(),
        }
    except requests.RequestException:
        return None


@st.cache_data(ttl=60)
def obtener_snapshot_tiendanube(store_id, token_ref, client_id, _progress_callback=None):
    def report(progress, message):
        if _progress_callback:
            _progress_callback(progress, message)

    report(0.05, "Iniciando sincronización con Tiendanube...")
    access_token = obtener_token_seguro(token_ref)
    normalized_store_id = normalizar_store_id(store_id)
    if not normalized_store_id or not access_token:
        report(1.0, "Store ID o token inválido.")
        return {"ok": False, "error": "invalid_store_id"}

    base_url = f"https://api.tiendanube.com/2025-03/{normalized_store_id}"
    
    # --- BLOQUE FINAL LIMPIO (Copia y pega esto sobre el anterior) ---
    headers = {
        "Authentication": f"bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "Flowmerce (walvarezc2@unemi.edu.ec)"
    }
    # ----------------------------------------------------------------
    session = get_http_session()
    try:
        max_pages = 5
        product_share = 0.7
        orders_share = 0.25
        base_progress = 0.05

        products = []
        page = 1
        while True:
            report(
                base_progress + (page - 1) / max_pages * product_share,
                f"Descargando productos, página {page} de {max_pages}...",
            )
            r_products = session.get(
                f"{base_url}/products",
                headers=headers,
                params={"page": page, "per_page": 50},
                timeout=10,
            )
            if r_products.status_code == 401:
                report(1.0, "Token no autorizado.")
                return {"ok": False, "error": "unauthorized"}
            if r_products.status_code == 429:
                report(1.0, "Límite de llamadas alcanzado.")
                return {"ok": False, "error": "rate_limit"}
            if r_products.status_code != 200:
                report(1.0, "Error descargando productos.")
                return {"ok": False, "status_products": r_products.status_code}
            page_items = r_products.json() if isinstance(r_products.json(), list) else []
            products.extend(page_items)
            report(
                base_progress + min(page / max_pages, 1.0) * product_share,
                f"Productos acumulados: {len(products)}",
            )
            if len(page_items) < 50 or page >= 5:
                break
            page += 1

        orders = []
        page = 1
        while True:
            report(
                base_progress + product_share + (page - 1) / max_pages * orders_share,
                f"Descargando órdenes, página {page} de {max_pages}...",
            )
            r_orders = session.get(
                f"{base_url}/orders",
                headers=headers,
                params={"page": page, "per_page": 50},
                timeout=10,
            )
            if r_orders.status_code == 401:
                report(1.0, "Token no autorizado.")
                return {"ok": False, "error": "unauthorized"}
            if r_orders.status_code == 429:
                report(1.0, "Límite de llamadas alcanzado.")
                return {"ok": False, "error": "rate_limit"}
            if r_orders.status_code != 200:
                report(1.0, "Error descargando órdenes.")
                return {"ok": False, "status_orders": r_orders.status_code}
            page_items = r_orders.json() if isinstance(r_orders.json(), list) else []
            orders.extend(page_items)
            report(
                base_progress + product_share + min(page / max_pages, 1.0) * orders_share,
                f"Órdenes acumuladas: {len(orders)}",
            )
            if len(page_items) < 50 or page >= 5:
                break
            page += 1

        total_orders = len(orders)
        paid_orders = sum(
            1 for o in orders if str(o.get("payment_status", "")).lower() == "paid"
        )
        report(1.0, "Sincronización completada.")
        return {
            "ok": True,
            "products": products,
            "products_count": len(products),
            "orders_count": total_orders,
            "paid_rate": (paid_orders / total_orders * 100) if total_orders else 0.0,
        }
    except requests.RequestException:
        report(1.0, "Error de red durante la sincronización.")
        return {"ok": False, "error": "network"}


def extraer_inventario_desde_snapshot(snapshot):
    products = snapshot.get("products", []) if snapshot else []
    rows = []
    for p in products:
        nombre = p.get("name", {})
        if isinstance(nombre, dict):
            nombre = (
                nombre.get("es")
                or nombre.get("pt")
                or nombre.get("en")
                or p.get("handle")
                or "Producto"
            )
        nombre = str(nombre) if nombre else "Producto"
        variants = p.get("variants", []) if isinstance(p.get("variants", []), list) else []
        stock_total = (
            sum(int(v.get("stock", 0) or 0) for v in variants)
            if variants
            else int(p.get("stock", 0) or 0)
        )
        rows.append(
            {
                "Producto": nombre,
                "Stock": max(0, stock_total),
                "Ventas_30d": 0,
                "Ventas_7d": 0,
                "Costo": 0,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=["Producto", "Stock", "Ventas_30d", "Ventas_7d", "Costo"]
        )
    return pd.DataFrame(rows)


async def obtener_snapshot_tiendanube_async(
    store_id, token_ref, client_id, _progress_callback=None
):
    # Run network-bound sync in a worker thread to keep Streamlit responsive.
    return await asyncio.to_thread(
        obtener_snapshot_tiendanube,
        store_id,
        token_ref,
        client_id,
        _progress_callback,
    )
