from backend.database import supabase

def create_product(store_id, name, price, description):
    response = supabase.table("products").insert({
        "store_id": store_id,
        "name": name,
        "price": price,
        "description": description
    }).execute()
    return response.data

def get_products(store_id):
    response = supabase.table("products") \
        .select("*") \
        .eq("store_id", store_id) \
        .order("created_at", desc=True) \
        .execute()
    return response.data
