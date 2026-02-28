from fastapi import APIRouter

from backend.database import supabase

router = APIRouter()


def create_order(store_id, customer_name, item_name, quantity, total_amount, status="pending"):
    response = (
        supabase.table("orders")
        .insert(
            {
                "store_id": store_id,
                "customer_name": customer_name,
                "item_name": item_name,
                "quantity": quantity,
                "total_amount": total_amount,
                "status": status,
            }
        )
        .execute()
    )
    return response.data


def list_orders_for_store(store_id):
    response = (
        supabase.table("orders")
        .select("*")
        .eq("store_id", store_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def update_order_status(order_id, store_id, status):
    response = (
        supabase.table("orders")
        .update({"status": status})
        .eq("id", order_id)
        .eq("store_id", store_id)
        .execute()
    )
    return response.data


@router.post("/")
def create_order_route(data: dict):
    return create_order(
        data["store_id"],
        data["customer_name"],
        data["item_name"],
        data["quantity"],
        data["total_amount"],
        data.get("status", "pending"),
    )


@router.get("/")
def list_orders(store_id: str):
    return list_orders_for_store(store_id)


@router.patch("/{order_id}")
def patch_order_status(order_id: str, store_id: str, status: str):
    return update_order_status(order_id, store_id, status)
