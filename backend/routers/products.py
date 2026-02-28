from fastapi import APIRouter

from backend.database import supabase

router = APIRouter()


def create_product(store_id, name, price, description):
    response = (
        supabase.table("products")
        .insert(
            {
                "store_id": store_id,
                "name": name,
                "price": price,
                "description": description,
            }
        )
        .execute()
    )
    return response.data


def get_products(store_id):
    response = (
        supabase.table("products")
        .select("*")
        .eq("store_id", store_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def delete_product(product_id, store_id):
    response = (
        supabase.table("products")
        .delete()
        .eq("id", product_id)
        .eq("store_id", store_id)
        .execute()
    )
    return response.data


@router.get("/")
def list_products(store_id: str):
    return get_products(store_id)


@router.post("/")
def create_product_route(data: dict):
    return create_product(
        data["store_id"],
        data["name"],
        data["price"],
        data.get("description", ""),
    )


@router.delete("/{product_id}")
def delete_product_route(product_id: str, store_id: str):
    return delete_product(product_id, store_id)
