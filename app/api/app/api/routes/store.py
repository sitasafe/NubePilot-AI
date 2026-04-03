from fastapi import APIRouter, Depends, HTTPException
from app.services.tiendanube import obtener_snapshot_tiendanube

router = APIRouter()

@router.get("/inventory/{store_id}")
async def get_store_inventory(store_id: str, token_ref: str):
    # Aquí llamamos a la lógica que ya tienes en services
    data = obtener_snapshot_tiendanube(store_id, token_ref, "27483")
    if not data.get("ok"):
        raise HTTPException(status_code=400, detail=data.get("error"))
    return data
    