from fastapi import APIRouter
from backend.database import supabase

router = APIRouter()

@router.post("/")
def create_order(data: dict):
    response = supabase.table("orders").insert(data).execute()
    return response.data

@router.get("/")
def list_orders(store_id: str):
    response = supabase.table("orders").select("*").eq("store_id", store_id).execute()
    return response.data
