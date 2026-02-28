from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter

from backend.config import JWT_SECRET
from backend.database import supabase

router = APIRouter()


def create_jwt(payload: dict):
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def signup_user(email: str, password: str, store_name: str):
    if not store_name or not store_name.strip():
        return "STORE_NAME_EMPTY", None

    existing = supabase.table("users").select("id").eq("email", email).execute()
    if existing.data:
        return "EMAIL_EXISTS", None

    store = supabase.table("stores").insert({"name": store_name.strip()}).execute()
    store_id = store.data[0]["id"]

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = supabase.table("users").insert(
        {
            "email": email,
            "password_hash": password_hash,
            "store_id": store_id,
        }
    ).execute()

    token = create_jwt({"user_id": user.data[0]["id"], "store_id": store_id})
    return token, store_id


def login_user(email: str, password: str):
    response = supabase.table("users").select("*").eq("email", email).execute()
    if not response.data:
        return None, None

    user = response.data[0]
    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return None, None

    token = create_jwt({"user_id": user["id"], "store_id": user["store_id"]})
    return token, user["store_id"]
