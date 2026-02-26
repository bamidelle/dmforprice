from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import jwt
import bcrypt

from backend.database import supabase
from backend.config import JWT_SECRET

router = APIRouter()

# -------------------------
# JWT Helpers
# -------------------------

def create_jwt(payload: dict):
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


# =========================
# STREAMLIT-FRIENDLY HELPERS
# =========================

def signup_user(email: str, password: str, store_name: str):

    # 🔐 Hash password properly
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create store
    store = supabase.table("stores").insert({
        "name": store_name
    }).execute()

    store_id = store.data[0]["id"]

    # Create user with hashed password
    user = supabase.table("users").insert({
        "email": email,
        "password_hash": password_hash,
        "store_id": store_id
    }).execute()

    token = create_jwt({
        "user_id": user.data[0]["id"],
        "store_id": store_id
    })

    return token, store_id


def login_user(email: str, password: str):

    # Fetch single user
    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .single()
        .execute()
    )

    if not response.data:
        return None, None

    user = response.data

    stored_hash = user["password_hash"]

    # 🔐 Verify password correctly
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8")
    ):
        return None, None

    # Create JWT
    token = jwt.encode(
        {
            "user_id": user["id"],
            "store_id": user["store_id"],
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return token, user["store_id"]
