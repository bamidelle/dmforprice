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

    stored_hash = user.get("password_hash")
    legacy_password = user.get("password")

    is_valid_password = False

    if isinstance(stored_hash, (str, bytes)):
        hash_bytes = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode("utf-8")
        try:
            is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hash_bytes)
        except ValueError:
            is_valid_password = False
    elif isinstance(legacy_password, str):
        # Backward compatibility for old records that stored plaintext passwords.
        is_valid_password = password == legacy_password
    if stored_hash is None:
        # Backward compatibility for old records that stored plaintext passwords.
        stored_hash = user.get("password")

    if not isinstance(stored_hash, (str, bytes)):
        return None, None

    hash_bytes = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode("utf-8")

    try:
        is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hash_bytes)
    except ValueError:
        return None, None

    if not is_valid_password:
        return None, None

    token = create_jwt({"user_id": user["id"], "store_id": user["store_id"]})
    return token, user["store_id"]
