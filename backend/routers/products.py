from fastapi import APIRouter
from backend.database import supabase

router = APIRouter()

@router.post("/")
def create_product(data: dict):
    response = supabase.table("products").insert(data).execute()
    return response.data

@router.get("/")
def list_products(store_id: str):
    response = supabase.table("products").select("*").eq("store_id", store_id).execute()
    return response.data

@router.get("/")
def list_products(user=Depends(get_current_user)):
    store_id = user["store_id"]
